from django.contrib.auth.base_user import BaseUserManager

from meetups_backend.exceptions import UniqueRecordExistsException


class DbUserManager(BaseUserManager):
    """
    This class represents a manager for all users of the app.
    Manager is an interface between the model and the DB.
    """

    def create_user(self, email: str, password: str, **kwargs):
        """
        Creates and saves new user to the DB.
        """
        # ensure that there is no record with the given email
        email: str = self.normalize_email(email)
        if self.filter(email=email).exists():
            raise UniqueRecordExistsException(f'User with email {email} already exists.')

        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user
