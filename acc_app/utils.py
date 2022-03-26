from random import randint
from django.core.mail import EmailMessage
from django.core.cache import cache

class Utils:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()

    def send_otp_mobile(phone, user):
        if cache.get(phone):
            return False, cache._has_expired(phone)
        
        try:
            generate_otp = randint(1000, 9999)
            cache.set(phone, generate_otp, timeout = 60)
            user.phone_otp = generate_otp
            print(generate_otp)
            user.save()

            return True, 0

        except Exception as e:
            print(e)
