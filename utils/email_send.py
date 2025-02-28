from users.models import EmailVerifyRecord
from django.core.mail import send_mail
import random
import string

def random_str(randomlength=8):
    """ Method of generating a random string of 8 digits """
    chars = string.ascii_letters + string.digits   # Generates the a-zA-Z0-9 string
    strcode = ''.join(random.sample(chars, randomlength))  # Generates a random 8-digit string
    return strcode

def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = random_str()
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    # email_record.add_time = datetime.now()
    email_record.save()

    if send_type == 'register':
        email_title = 'Blog registration activation link'
        email_body = 'Please click the link below to activate your account: http://127.0.0.1:8000/users/active/{0}'.format(code)

        send_status = send_mail(email_title, email_body, 'gaogao20021030@163.com', [email])
        if send_status:
            pass

    elif send_type == 'forget':
        email_title = 'Retrieve password link'
        email_body = 'Please click the link below to change your password: http://127.0.0.1:8000/users/forget_pwd_url/{0}'.format(code)

        send_status = send_mail(email_title, email_body, '15336112587@163.com', [email])
        if send_status:
            pass