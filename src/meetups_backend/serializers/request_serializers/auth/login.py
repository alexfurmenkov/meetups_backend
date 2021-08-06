from rest_framework.serializers import Serializer, CharField, EmailField

from meetups_backend.constants import PASSWORD_MIN_LENGTH


class LoginSerializer(Serializer):
    """
    Serializer for POST HTTP request on URL "/auth/login"
    """

    email = EmailField(required=True, label='email')
    password = CharField(required=True, label='password', min_length=PASSWORD_MIN_LENGTH)
