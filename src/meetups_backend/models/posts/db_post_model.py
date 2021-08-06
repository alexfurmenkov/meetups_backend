from django.db.models import Model, CharField, TextField, ForeignKey, CASCADE, OneToOneField

from .db_post_address_model import DbPostAddressModel
from .db_post_type_model import DbPostTypeModel
from ..users.db_user_model import DbUserModel
from ..base_db_model import BaseDbModel


class DbPostModel(BaseDbModel, Model):
    """
    This class represents a post database record.
    """
    class Meta:
        db_table = 'posts'

    user = ForeignKey(to=DbUserModel, on_delete=CASCADE, name='user')
    type = ForeignKey(to=DbPostTypeModel, on_delete=CASCADE, name='type')
    address = OneToOneField(to=DbPostAddressModel, on_delete=CASCADE, name='address')
    name = CharField(name='name', max_length=1000)
    description = TextField(name='description')

    @property
    def _update_allowed_fields(self) -> list:
        return [
            'name',
            'description',
            'type',
        ]

    def update_db_record(self, update_body: dict):
        """
        Extends the method of parent class.
        Reason - Need to get type object from the DB if type is being updated.
        :param update_body: Dict with keys to be updated
        :return: None
        """
        type_id: str = update_body.get('type', None)
        if type_id:
            update_body['type'] = DbPostTypeModel.objects.get(id=type_id)
        super(DbPostModel, self).update_db_record(update_body)

    def __str__(self):
        return self.name
