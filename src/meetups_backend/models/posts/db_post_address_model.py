from django.db.models import Model, CharField

from ..base_db_model import BaseDbModel


class DbPostAddressModel(BaseDbModel, Model):
    """
    This class represents a post address database record.
    """
    class Meta:
        db_table = 'posts_addresses'

    country = CharField(name='country', max_length=1000)
    city = CharField(name='city', max_length=1000)
    street = CharField(name='street', max_length=1000)
    house_no = CharField(name='house_no', max_length=1000)
    floor = CharField(name='floor', blank=True, default='', max_length=1000)

    @property
    def _update_allowed_fields(self) -> list:
        return [
            'country',
            'city',
            'street',
            'house_no',
            'floor',
        ]
