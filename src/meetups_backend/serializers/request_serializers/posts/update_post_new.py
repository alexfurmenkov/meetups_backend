from rest_framework.serializers import Serializer, CharField


class UpdatePostDetailsSerializer(Serializer):
    """
    This serializer defines necessary fields that should be
    passed to create a new post DB record.
    """
    name = CharField(required=False, label='name')
    description = CharField(required=False, label='description')
    type = CharField(required=False, label='type')


class UpdatePostAddressSerializer(Serializer):
    """
    This serializer defines necessary fields that should be
    passed to create a new post address DB record.
    """
    country = CharField(required=False, label='country')
    city = CharField(required=False, label='city')
    street = CharField(required=False, label='street')
    house_no = CharField(required=False, label='house_no')
    floor = CharField(required=False, label='floor')


class UpdatePostSerializerNew(Serializer):
    """
    Serializer for request on PUT "/posts/" endpoint.
    The serializer consists of two nested serializers because
    of the request body structure (see API docs in the docs directory).
    """
    post_details = UpdatePostDetailsSerializer()
    address = UpdatePostAddressSerializer()
