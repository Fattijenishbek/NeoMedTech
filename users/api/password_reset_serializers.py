from rest_auth.serializers import PasswordResetSerializer as _PasswordResetSerializer
from django.conf import settings


class PasswordResetSerializer(_PasswordResetSerializer):
    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),

            'email_template_name': 'reset_password.html',

            'request': request
        }
        self.reset_form.save(**opts)