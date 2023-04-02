from django.contrib.auth.tokens import PasswordResetTokenGenerator
from . import views

from six import text_type

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self,user,timestamp):
        return (
        text_type(views.EMAIL) + text_type(timestamp) 
        # text_type(user.profile.signup_confirmation)
        )

generate_token = TokenGenerator()