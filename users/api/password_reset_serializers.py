from medtech import settings
from rest_auth.serializers import PasswordResetSerializer as _PasswordResetSerializer

class PasswordResetSerializer(_PasswordResetSerializer):
    def save(self):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'EMAIL_HOST_USER'),

            'email_template_name': 'reset_password.html',

            'request': request
        }
        self.reset_form.save(**opts)