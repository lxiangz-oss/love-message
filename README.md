# love-message

An automated daily email project powered by GitHub Actions.

It generates weather info, relationship countdowns, and a short message, then sends an email via Gmail.

## Files

- `send_message.py`: main script
- `.github/workflows/daily-message.yml`: schedule + manual trigger
- `preview.py`: local HTML preview (no email sent)

## Usage

### Local preview (no send)

```bash
python3 preview.py
```

### GitHub Actions send

Add these repository secrets in:
`Settings -> Secrets and variables -> Actions`

- `FROM_EMAIL`
- `TO_EMAIL`
- `GMAIL_PASSWORD`
- `CLAUDE_KEY`

Then manually run the `每日情书` workflow once to verify.

## Security

- Never hardcode real credentials in code.
- Keep all sensitive values in GitHub Secrets.
