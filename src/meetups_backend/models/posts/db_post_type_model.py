from django.db.models import Model, CharField, TextField

from ..base_db_model import BaseDbModel


class DbPostTypeModel(BaseDbModel, Model):
    """
    This class represents a post type database record.
    """
    class Meta:
        db_table = 'post_type'

    name = CharField(name='name', max_length=1000)
    description = TextField(name='description')

    @property
    def _update_allowed_fields(self) -> list:
        return [
            'name',
            'description',
        ]

    def __str__(self):
        return self.name
