# MailHog (local SMTP) — Development guide

This project includes a MailHog service for local SMTP testing.

Quick start (Docker):

1. Start MailHog:
   ```bash
   docker run -d --name mailhog -p 1025:1025 -p 8025:8025 mailhog/mailhog:latest
   ```
2. Add or copy dev env vars (use `backend/.env.dev` which already contains MailHog values):
   - `MAIL_SERVER=mailhog`
   - `MAIL_PORT=1025`
   - `MAIL_USE_TLS=False`
   - `MAIL_OUTPUT_DIR=/app/backend/instance/sent_emails` (optional)

3. Send a test email using the project's helper script (runs within virtualenv):
   ```powershell
   $env:MAIL_SERVER='localhost'; $env:MAIL_PORT='1025'; $env:MAIL_USE_TLS='False'
   .venv\Scripts\python backend/scripts/send_test_email.py --to test@example.com --subject "MailHog test" --body "Hello" 
   # Or use the direct SMTP test helper which exercises real SMTP connection code:
   .venv\Scripts\python backend/scripts/send_test_email_smtp.py --to test@example.com --subject "MailHog test" --body "Hello"
   ```

4. Open MailHog UI to view messages: http://localhost:8025

Fallback: run a small Python SMTP debug server (no Docker required)

If you cannot run Docker or prefer not to, you can run a tiny SMTP debug server that
prints every received message to your terminal. A helper script is included:

From the repo root:

- Run the server:
  ```powershell
  # Windows / PowerShell
  .venv\Scripts\python backend/scripts/run_smtp_debug_server.py --host 127.0.0.1 --port 1025
  ```
  or on POSIX:
  ```bash
  python backend/scripts/run_smtp_debug_server.py --host 127.0.0.1 --port 1025
  ```

- In another terminal, configure env vars for your test run and send a test email:
  ```powershell
  $env:MAIL_SERVER='localhost'; $env:MAIL_PORT='1025'; $env:MAIL_USE_TLS='False'
  .venv\Scripts\python backend/scripts/send_test_email.py --to test@example.com --subject "Local SMTP test" --body "Hello"
  ```

- Or run the one-shot demo (starts an in-process debug server, sends a test via the app, prints results):
  ```powershell
  # Windows
  .venv\Scripts\Activate.ps1
  .\backend\scripts\local_smtp_demo.ps1 -To test@example.com -Port 2505
  ```
  or on POSIX:
  ```bash
  .venv/bin/python backend/scripts/local_smtp_demo.py --to test@example.com --port 2505
  ```

The SMTP debug server will print the message content to the terminal where it's running.

Makefile helpers (backend):
- `make mailhog-up` — starts a MailHog container
- `make mailhog-down` — removes MailHog container

Notes:
- If `MAIL_SERVER` is not configured, the app falls back to writing `.eml` files to `MAIL_OUTPUT_DIR` (default: `instance/sent_emails`).
- You can explicitly set the sender address with `MAIL_FROM` or `SMTP_FROM` to control the From header used in both SMTP and file fallback.
- For production use, configure a real SMTP provider (SendGrid/Mailgun/AWS SES) and set `SMTP_*` or `MAIL_*` environment variables.
