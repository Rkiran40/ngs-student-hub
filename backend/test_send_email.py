import os
import sys
from pathlib import Path

# Ensure we can import the backend package when running this file directly
project_root = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(project_root))

# Ensure mail saved to backend/mail_out
os.environ.pop('MAIL_SERVER', None)
mail_out_dir = Path(__file__).parent / 'mail_out'
os.environ['MAIL_OUTPUT_DIR'] = str(mail_out_dir)

from backend.email_utils import send_email

print('Mail output dir:', os.environ['MAIL_OUTPUT_DIR'])
res = send_email('devtest@example.com', 'Test OTP', 'This is a test OTP email body')
print('send_email returned:', res)

print('mail_out contents:')
for p in sorted(mail_out_dir.glob('*.eml')):
    print('-', p.name)
    print(p.read_text()[:400])
