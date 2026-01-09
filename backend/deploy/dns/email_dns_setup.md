# SPF / DKIM / DMARC setup for StudentHub transactional email

Use a dedicated sending subdomain (recommended): e.g., `mail.example.com` or `mta.example.com`.

## SPF
- Purpose: authorize sending hosts for your domain/subdomain.
- Example record for `example.com` allowing SendGrid and your own SMTP host:

```
Type: TXT
Name: example.com
Value: "v=spf1 include:sendgrid.net ip4:203.0.113.4 -all"
```

- If you're using a subdomain `mail.example.com` and sending from `no-reply@mail.example.com`, add the TXT on the parent domain or subdomain accordingly.

## DKIM
- Purpose: cryptographic signing of outgoing mail to prove origin.
- Steps:
  1. Generate DKIM keys (or use provider-provided keys).
  2. Add a TXT record with the selector you choose. Example (selector `s1`):

```
Type: TXT
Name: s1._domainkey.example.com
Value: "v=DKIM1; k=rsa; p=MIIBIjANBgkq..."
```

- Provider-managed: many providers (SendGrid, Mailgun) give you a selector and key pair and will sign outgoing mail for you.
- Verify using `dig` or online checkers and by inspecting the `DKIM-Signature` header on a received message.

## DMARC
- Purpose: policy for how to treat unauthenticated mail and where to send aggregate reports.
- Start with a monitoring policy and then move to enforcement:

```
Type: TXT
Name: _dmarc.example.com
Value: "v=DMARC1; p=none; rua=mailto:dmarc-aggregate@example.com; ruf=mailto:dmarc-forensic@example.com; pct=100"
```

- After monitoring, change `p=none` to `p=quarantine` or `p=reject` once you're confident legitimate mail is passing SPF/DKIM.

## Verification
- Send a test email and inspect headers (`Authentication-Results`, `DKIM-Signature`, `Received-SPF`).
- Use online tools (MXToolbox, Mail-Tester) or `openssl s_client` / `dig` to verify records.

## Notes
- Use a consistent `From` address that matches your domain (e.g., `no-reply@mail.example.com`).
- If using Gmail as SMTP (personal Gmail), SPF/DKIM for sending domain is out of your control—using Gmail for transactional email is discouraged in production.
- For high deliverability, use a transactional provider and follow their onboarding steps for DKIM verification.