import os, ssl, smtplib, traceback

# Simple .env parser (avoid python-dotenv dependency for this check)
mail = {}
with open('backend/.env', 'r', encoding='utf-8') as f:
    for line in f:
        line=line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' in line:
            k,v=line.split('=',1)
            mail[k.strip()]=v.strip()
server=mail.get('MAIL_SERVER') or mail.get('SMTP_SERVER')
port=int(mail.get('MAIL_PORT') or mail.get('SMTP_PORT') or 587)
user=mail.get('MAIL_USERNAME')
password=mail.get('MAIL_PASSWORD')
print('Server', server, 'Port', port, 'User', user)
try:
    s=smtplib.SMTP(server, port, timeout=10)
    s.set_debuglevel(1)
    s.starttls(context=ssl.create_default_context())
    s.login(user, password)
    s.sendmail(user, ['rkiran63096@gmail.com'], 'To: rkiran63096@gmail.com\nSubject: debug\n\nbody')
    s.quit()
    print('OK send')
except Exception:
    traceback.print_exc()