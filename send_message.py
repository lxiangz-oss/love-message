import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date
import requests
import anthropic

# --- 配置区（见面日期可以随时改这里）---
FROM_EMAIL = "<YOUR_FROM_EMAIL>"
TO_EMAIL = "<YOUR_TO_EMAIL>"
ANNIVERSARY = date(2021, 12, 25)       # 纪念日
NEXT_MEETING = date(2026, 3, 10)       # 下次见面日期，改这里

# --- API Keys（从 GitHub Secrets 环境变量读取）---
CLAUDE_KEY = os.environ["CLAUDE_KEY"]
GMAIL_PASSWORD = os.environ["GMAIL_PASSWORD"]

# WMO 天气代码 → 中文描述
WMO_CODE = {
    0: "晴", 1: "晴", 2: "多云", 3: "阴",
    45: "雾", 48: "雾",
    51: "小毛毛雨", 53: "毛毛雨", 55: "大毛毛雨",
    61: "小雨", 63: "中雨", 65: "大雨",
    71: "小雪", 73: "中雪", 75: "大雪", 77: "雪粒",
    80: "阵雨", 81: "中阵雨", 82: "强阵雨",
    85: "阵雪", 86: "强阵雪",
    95: "雷阵雨", 96: "雷雨夹冰雹", 99: "强雷雨夹冰雹",
}


def get_weather(city_name, lat, lon):
    """获取城市实时天气（Open-Meteo，无需 API Key）"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,apparent_temperature,weather_code",
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        current = data["current"]
        return {
            "temp": round(current["temperature_2m"], 1),
            "feelsLike": round(current["apparent_temperature"], 1),
            "text": WMO_CODE.get(current["weather_code"], "未知"),
        }
    except Exception as e:
        print(f"天气获取失败 {city_name}: {e}")
    return {"temp": "??", "text": "暂无数据", "feelsLike": "??"}


def get_romantic_quote():
    """用 Claude 生成幽默情话"""
    try:
        client = anthropic.Anthropic(api_key=CLAUDE_KEY)
        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=150,
            messages=[
                {
                    "role": "user",
                    "content": (
                        "请用中文生成一句幽默甜蜜的情话，"
                        "风格轻松有趣不油腻，像朋友之间温柔的调侃，"
                        "50字以内，只输出情话本身，不要加引号或其他内容。"
                    ),
                }
            ],
        )
        return msg.content[0].text.strip()
    except Exception as e:
        print(f"Claude API 失败: {e}")
        return "今天也要好好吃饭，毕竟我还没能帮你刷碗。"


def build_html(today, days_together, days_until_meeting, durham, boston, quote):
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body style="font-family: 'Helvetica Neue', Arial, sans-serif; max-width: 540px; margin: 0 auto;
             padding: 24px 16px; background-color: #fafafa; color: #333;">

  <!-- 标题 -->
  <div style="text-align: center; margin-bottom: 24px;">
    <h2 style="color: #d4526e; margin: 0; font-size: 22px;">早安 ☀️</h2>
    <p style="color: #bbb; font-size: 13px; margin: 6px 0 0;">{today.strftime('%Y年%m月%d日')}</p>
  </div>

  <!-- 天气 -->
  <div style="background: white; border-radius: 16px; padding: 20px 16px;
              margin-bottom: 14px; box-shadow: 0 1px 6px rgba(0,0,0,0.07);">
    <p style="margin: 0 0 16px; font-weight: bold; color: #555; font-size: 14px;">🌤 今日天气</p>
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td style="width: 50%; text-align: center; padding: 4px 8px;">
          <p style="margin: 0; font-size: 12px; color: #aaa;">📍 Durham, NC</p>
          <p style="margin: 8px 0 4px; font-size: 36px; font-weight: bold; color: #333; line-height: 1;">
            {durham['temp']}°C
          </p>
          <p style="margin: 0; color: #666; font-size: 14px;">{durham['text']}</p>
          <p style="margin: 4px 0 0; font-size: 11px; color: #bbb;">体感 {durham['feelsLike']}°C</p>
        </td>
        <td style="width: 1px; background: #f0f0f0; padding: 0;"></td>
        <td style="width: 50%; text-align: center; padding: 4px 8px;">
          <p style="margin: 0; font-size: 12px; color: #aaa;">📍 Boston, MA</p>
          <p style="margin: 8px 0 4px; font-size: 36px; font-weight: bold; color: #333; line-height: 1;">
            {boston['temp']}°C
          </p>
          <p style="margin: 0; color: #666; font-size: 14px;">{boston['text']}</p>
          <p style="margin: 4px 0 0; font-size: 11px; color: #bbb;">体感 {boston['feelsLike']}°C</p>
        </td>
      </tr>
    </table>
  </div>

  <!-- 倒计时 -->
  <div style="background: white; border-radius: 16px; padding: 20px 16px;
              margin-bottom: 14px; box-shadow: 0 1px 6px rgba(0,0,0,0.07);">
    <p style="margin: 0 0 16px; font-weight: bold; color: #555; font-size: 14px;">💕 我们的时间</p>
    <table width="100%" cellpadding="0" cellspacing="0">
      <tr>
        <td style="width: 50%; text-align: center; padding: 4px 8px;">
          <p style="margin: 0; font-size: 12px; color: #aaa;">在一起</p>
          <p style="margin: 8px 0 4px; font-size: 40px; font-weight: bold; color: #d4526e; line-height: 1;">
            {days_together}
          </p>
          <p style="margin: 0; font-size: 12px; color: #aaa;">天</p>
        </td>
        <td style="width: 1px; background: #f0f0f0; padding: 0;"></td>
        <td style="width: 50%; text-align: center; padding: 4px 8px;">
          <p style="margin: 0; font-size: 12px; color: #aaa;">距离见面还有</p>
          <p style="margin: 8px 0 4px; font-size: 40px; font-weight: bold; color: #d4526e; line-height: 1;">
            {days_until_meeting}
          </p>
          <p style="margin: 0; font-size: 12px; color: #aaa;">天</p>
        </td>
      </tr>
    </table>
  </div>

  <!-- 情话 -->
  <div style="background: white; border-radius: 16px; padding: 20px 16px;
              margin-bottom: 14px; box-shadow: 0 1px 6px rgba(0,0,0,0.07);">
    <p style="margin: 0 0 12px; font-weight: bold; color: #555; font-size: 14px;">💬 今日情话</p>
    <p style="margin: 0; font-size: 15px; color: #555; line-height: 1.8;
              text-align: center; font-style: italic; padding: 0 8px;">
      {quote}
    </p>
  </div>

  <!-- 签名 -->
  <p style="text-align: center; color: #ccc; font-size: 12px; margin-top: 20px;">
    From 斑点狗 🐾
  </p>

</body>
</html>"""


def main():
    today = date.today()
    days_together = (today - ANNIVERSARY).days
    days_until_meeting = (NEXT_MEETING - today).days

    print(f"📅 今天: {today} | 在一起: {days_together}天 | 距离见面: {days_until_meeting}天")

    durham = get_weather("Durham", 35.9940, -78.8986)
    boston = get_weather("Boston", 42.3601, -71.0589)
    print(f"🌤 Durham: {durham['temp']}°C {durham['text']}")
    print(f"🌤 Boston: {boston['temp']}°C {boston['text']}")

    quote = get_romantic_quote()
    print(f"💬 情话: {quote}")

    html = build_html(today, days_together, days_until_meeting, durham, boston, quote)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "From 斑点狗"
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL
    msg.attach(MIMEText(html, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(FROM_EMAIL, GMAIL_PASSWORD)
        server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())

    print("✅ 邮件发送成功！")


if __name__ == "__main__":
    main()
