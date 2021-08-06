from rest_framework.serializers import Serializer, CharField, EmailField

from meetups_backend.constants import PASSWORD_MIN_LENGTH, BIO_MAX_LENGTH


class CreateNewUserSerializer(Serializer):
    """
    Serializer for POST HTTP request on URL "/users/"
    """

    email = EmailField(required=True, label='email')
    password = CharField(required=True, label='password', min_length=PASSWORD_MIN_LENGTH)
    bio = CharField(required=True, label='bio', max_length=BIO_MAX_LENGTH)
