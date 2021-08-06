from rest_framework.serializers import ModelSerializer

from meetups_backend.models import DbPostTypeModel


class DbPostTypeModelSerializer(ModelSerializer):
    """
    Serializer for post type model.
    """

    class Meta:
        model = DbPostTypeModel
        fields: list = [
            'id',
            'name',
            'description',
        ]
