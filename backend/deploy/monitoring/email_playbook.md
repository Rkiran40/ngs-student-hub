# Email alert playbook

## StudentHubEmailFailures (warning)
- Trigger: `StudentHubEmailFailures` (rate(studenthub_emails_failed_total[5m]) > 0 for 5m)
- Severity: warning
- Initial steps:
  1. Check `/metrics` to confirm `studenthub_emails_failed_total` increment.
  2. Check application logs around the failure time (`journalctl` or centralized logging) for SMTP errors.
  3. Verify SMTP provider connectivity and credentials by running the CLI test: `python backend/scripts/send_test_email.py --to you@domain.com`.
  4. If errors indicate authentication, rotate SMTP credentials and re-test.
- Escalation: If failure persists for >15m or matches `StudentHubEmailFailureSpike`, escalate to on-call and mark `severity: critical`.

## StudentHubEmailFailureSpike (critical)
- Trigger: `StudentHubEmailFailureSpike` (increase > 10 over 15m)
- Severity: critical
- Steps:
  1. Confirm spike using Prometheus graph and logs for correlated errors.
  2. Check provider status page (SendGrid/Mailgun/AWS SES/etc.) for incidents.
  3. Check recent deploys or configuration changes (SMTP env, DNS changes such as SPF/DKIM, or firewall rules).
  4. If provider outage, consider emergency fallback (e.g., queue emails for later retry) and notify stakeholders.
  5. After fix, monitor metrics for recovery and close the alert.