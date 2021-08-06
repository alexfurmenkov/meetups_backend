from django.test import TestCase

from meetups_backend.exceptions import UniqueRecordExistsException
from meetups_backend.models import DbUserModel
from tests.utils.test_records_pks import TEST_USER_PK


class TestDbUserModel(TestCase):
    """
    This class contains tests for the db user model.
    """

    fixtures = ['test_user.json', ]

    def setUp(self) -> None:
        """
        A method which is launched before every test.
        """
        self.user: DbUserModel = DbUserModel.objects.get(pk=TEST_USER_PK)

    def test_create_user(self):
        """
        The test checks creation of new user.
        """
        email: str = 'test@mail.com'
        password: str = 'test_password'
        bio: str = 'test bio'
        new_user: DbUserModel = DbUserModel.objects.create_user(email, password, bio=bio)
        assert email == new_user.email
        assert bio == new_user.bio
        assert new_user.id is not None

    def test_create_user_existing_user(self):
        """
        Test checks that user with the same email cannot be created.
        """
        with self.assertRaises(UniqueRecordExistsException):
            DbUserModel.objects.create_user(self.user.email, self.user.password, bio=self.user.bio)

    def test_update_user(self):
        """
        Test checks that only allowed fields can be updated.
        """
        new_bio: str = 'updated bio'
        new_email: str = 'updated_email@mail.ru'
        old_email: str = self.user.email

        # check that the attributes of an object have changed
        self.user.update_db_record({'bio': new_bio, 'email': new_email})
        assert self.user.bio == new_bio
        assert self.user.email == old_email
        assert self.user.email != new_email

        # check that the DB record has been updated
        updated_user: DbUserModel = DbUserModel.objects.get(id=self.user.id)
        assert updated_user.bio == new_bio
        assert updated_user.email == old_email
        assert updated_user.email != new_email
