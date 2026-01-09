# Secrets & SMTP credential management

## Best practices
- Do not commit secrets to the repository. Use environment variables or a secrets manager.
- Rotate SMTP credentials regularly and immediately after any suspected compromise.
- Prefer provider-managed API keys or app-specific passwords instead of primary account passwords.
- Limit access to production secrets and audit changes.

## GitHub Actions (example)
Use repository or organization secrets and reference them in workflows:

```yaml
# .github/workflows/deploy.yml (snippet)
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to server
        env:
          SMTP_SERVER: ${{ secrets.SMTP_SERVER }}
          SMTP_USER: ${{ secrets.SMTP_USER }}
          SMTP_PASSWORD: ${{ secrets.SMTP_PASSWORD }}
        run: |
          # Example: copy /etc/studenthub.env.template and inject secrets in CI deploy step
          ssh deploy@host "echo \"SMTP_SERVER=${SMTP_SERVER}\nSMTP_USER=${SMTP_USER}\nSMTP_PASSWORD=${SMTP_PASSWORD}\n\" > /etc/studenthub.env && sudo systemctl restart studenthub"
```

## AWS Secrets Manager example
- Store a secret JSON object: `{"SMTP_SERVER":"smtp.example.com","SMTP_USER":"u","SMTP_PASSWORD":"pw"}`
- Use IAM role on the host or ECS task to grant permission and fetch secrets at startup.

## Rotating credentials
1. Create new credentials in the SMTP provider (API key or app password).
2. Update the secret in your secrets manager or GitHub Secrets.
3. Deploy or restart the service to pick up new credentials.
4. Verify delivery by sending test emails and monitoring metrics.
5. Revoke old credentials once verified.

## Systemd note
If you place secrets in `/etc/studenthub.env`, make sure file permissions are strict (root:root, 600) and don't store secrets in a world-readable place.