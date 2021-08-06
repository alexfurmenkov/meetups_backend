from rest_framework.fields import CharField
from rest_framework.serializers import Serializer


class UpdatePostAddressSerializer(Serializer):
    country = CharField(required=False, label='country')
    city = CharField(required=False, label='city')
    street = CharField(required=False, label='street')
    house_no = CharField(required=False, label='house_no')
    floor = CharField(required=False, label='floor')
