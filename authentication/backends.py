import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)
        # auth_data = str(auth_data)

        if not auth_data:
            return None

        prefix, token = auth_data.decode('utf-8').split(' ')
        token = str(token)

        try:
            payload = jwt.decode(token, str(settings.JWT_SECRET_KEY), algorithms="HS256")

            user = User.objects.get(username=payload['username'])
            return (user, token)

        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed(
                'Your token is invalid,login')
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed(
                'Your token is expired,login')

        return super().authenticate(request)
