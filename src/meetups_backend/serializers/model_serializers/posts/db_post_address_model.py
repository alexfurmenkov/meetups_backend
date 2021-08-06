from rest_framework.serializers import ModelSerializer

from meetups_backend.models import DbPostAddressModel


class DbPostAddressModelSerializer(ModelSerializer):
    """
    Serializer for post address model.
    """

    class Meta:
        model = DbPostAddressModel
        fields: list = [
            'country',
            'city',
            'street',
            'house_no',
            'floor',
        ]
