from rest_framework.serializers import Serializer, CharField

from meetups_backend.constants import BIO_MAX_LENGTH


class UpdateUserSerializer(Serializer):
    """
    Serializer for PUT HTTP request on URL "/users/"
    """

    bio = CharField(required=False, label='bio', max_length=BIO_MAX_LENGTH)
