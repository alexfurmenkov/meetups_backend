from rest_framework.serializers import Serializer, CharField, UUIDField


class CreatePostDetailsSerializer(Serializer):
    """
    This serializer defines necessary fields that should be
    passed to create a new post DB record.
    """
    name = CharField(required=True, label='name')
    description = CharField(required=True, label='description')
    type = UUIDField(required=True, label='type')


class CreatePostAddressSerializer(Serializer):
    """
    This serializer defines necessary fields that should be
    passed to create a new post address DB record.
    """
    country = CharField(required=True, label='country')
    city = CharField(required=True, label='city')
    street = CharField(required=True, label='street')
    house_no = CharField(required=True, label='house_no')
    floor = CharField(required=False, label='floor')


class CreateNewPostSerializer(Serializer):
    """
    Serializer for request on POST "/posts/" endpoint.
    The serializer consists of two nested serializers because
    of the request body structure (see API docs in the docs directory).
    """
    post_details = CreatePostDetailsSerializer()
    address = CreatePostAddressSerializer()
