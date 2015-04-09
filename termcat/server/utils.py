import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), '..')))

from django.conf import settings
from django.core.mail import send_mail
from io import StringIO
from traceback import print_tb
import socket

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
import django
django.setup()

from paste.models import Paste

def handle_new_paste(data, remote_ip_addr):
    p = Paste(data=data, remote_ip_addr=remote_ip_addr)
    p.save()
    return p

def delete_paste(paste):
    print('Connection was reset, deleting', paste)

def print_exception(remote_addr, exc):
    """Prints and emails the exception given."""

    # Construct the exception message
    s = StringIO()
    print('An exception occurred processing a request from {}:'.format(remote_addr), file=s)
    print_tb(exc.__traceback__, file=s)
    print('{}: {}'.format(exc.__class__.__name__, str(exc)), file=s, end='')
    s.seek(0)

    # Print and send 
    message = s.getvalue()
    if settings.DEBUG:
        print(message, file=sys.stderr)
    else:
        if not send_exception_email(message):
            print('Error: Failed to send email to ADMINS', file=sys.stderr)

def send_exception_email(message):
    """Sends a given message using Django's error email facility."""

    hostname = socket.gethostname()
    if len(settings.ADMINS) == 0:
        return False
    admins = [email for name, email in settings.ADMINS]

    # We must fail silently here otherwise a loop may be entered trying to send
    # exception emails.
    send_mail('[termcat.io on {}] Exception raised during server request'.format(hostname),
              message, 'termcat@' + hostname, admins, fail_silently=True)
    return True

def _test_exc_handling():
    try:
        socket.foo()
    except Exception as e:
        print_exception('<console>', e)
