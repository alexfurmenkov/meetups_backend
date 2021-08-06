from rest_framework.serializers import ModelSerializer

from meetups_backend.models import DbUserModel


class DbUserModelSerializer(ModelSerializer):
    """
    Serializer for DbUserModel class.
    """

    class Meta:
        model = DbUserModel
        fields: list = [
            'id',
            'email',
            'bio',
            'created_at',
            'updated_at',
        ]
