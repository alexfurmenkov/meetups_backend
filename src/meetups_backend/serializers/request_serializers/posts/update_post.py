from rest_framework.serializers import Serializer, CharField


class UpdatePostSerializer(Serializer):
    """
    Serializer for request on PUT "/posts/{post_id}/" endpoint.
    """
    name = CharField(required=False, label='name')
    description = CharField(required=False, label='description')
    type = CharField(required=False, label='type')
