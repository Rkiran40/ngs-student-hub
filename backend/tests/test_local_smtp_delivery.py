import os
import subprocess
import sys
import time
import socket
import pytest

SKIP_MSG = 'Integration test skipped: set RUN_SMTP_INTEGRATION_TESTS=1 to enable'

pytestmark = pytest.mark.skipif(os.environ.get('RUN_SMTP_INTEGRATION_TESTS') != '1', reason=SKIP_MSG)


def _wait_for_port(host, port, timeout=5.0):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except Exception:
            time.sleep(0.1)
    return False


def test_send_email_to_local_debug_server(tmp_path):
    host = '127.0.0.1'
    port = 2501  # test port (unlikely to be used)
    proc = subprocess.Popen([sys.executable, 'backend/scripts/run_smtp_debug_server.py', '--host', host, '--port', str(port)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    try:
        assert _wait_for_port(host, port, timeout=5.0), 'SMTP debug server did not start in time'

        # Run the test SMTP sender pointing to the local debug server
        env = os.environ.copy()
        env['MAIL_SERVER'] = host
        env['MAIL_PORT'] = str(port)
        env['MAIL_USE_TLS'] = 'False'

        p = subprocess.run([sys.executable, 'backend/scripts/send_test_email_smtp.py', '--to', 'test@example.com', '--subject', 'Integration Test', '--body', 'Hello from test'], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=10)
        # Ensure the sender succeeded
        assert p.returncode == 0, f"send script failed: {p.stdout}"

        # Read server output for the received message
        # Give the server a moment to flush its stdout
        time.sleep(0.5)
        out = proc.stdout.read()
        assert 'SMTP DEBUG SERVER RECEIVED MESSAGE' in out or 'Message:' in out
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=2)
        except Exception:
            proc.kill()
