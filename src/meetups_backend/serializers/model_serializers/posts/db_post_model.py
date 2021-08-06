from rest_framework.serializers import ModelSerializer

from meetups_backend.models import DbPostModel
from .db_post_address_model import DbPostAddressModelSerializer
from .db_post_type_model import DbPostTypeModelSerializer


class DbPostModelSerializer(ModelSerializer):
    """
    Serializer for post model.
    """
    address = DbPostAddressModelSerializer(many=False, read_only=True)
    type = DbPostTypeModelSerializer(many=False, read_only=True)

    class Meta:
        model = DbPostModel
        fields: list = [
            'id',
            'user_id',
            'address',
            'name',
            'description',
            'type',
        ]
