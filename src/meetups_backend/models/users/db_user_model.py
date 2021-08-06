from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models import EmailField, TextField

from ..base_db_model import BaseDbModel
from .db_user_manager import DbUserManager
from ...constants import BIO_MAX_LENGTH


class DbUserModel(BaseDbModel, AbstractBaseUser):
    """
    This class represents a user database record.
    Need to inherit from AbstractBaseUser to define
    custom username field and set of required fields.
    """
    class Meta:
        db_table = 'users'
        app_label = 'meetups_backend'

    email = EmailField(name='email', unique=True)
    bio = TextField(name='bio', max_length=BIO_MAX_LENGTH)

    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: list = ['bio']

    objects: DbUserManager = DbUserManager()

    @property
    def _update_allowed_fields(self) -> list:
        return [
            'bio',
        ]

    def __str__(self):
        return self.email
