from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


class Mailing:
    def __init__(self):
        self.sender = settings.EMAIL_HOST_USER

    def mail_reset_password(self, recipient, name, new_password):
        html = render_to_string(
            template_name='reset_password.html',
            context={
                'name_complete': name,
                'password': new_password
            }
        )
        return self.__send_mail(
            f'Reinicio de contraseña - {name}',
            [recipient],
            html
        )

    def __send_mail(self, subject, recipients, html):
        return send_mail(
            subject=subject,
            recipient_list=recipients,
            from_email=self.sender,
            html_message=html,
            message=None
        )
