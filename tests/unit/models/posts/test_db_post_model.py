import uuid

from django.test import TestCase

from meetups_backend.models import DbUserModel, DbPostAddressModel, DbPostModel, DbPostTypeModel
from tests.utils.test_records_pks import TEST_USER_PK, TEST_POST_PK, TEST_POST_ADDRESS_PK


class TestDbPostModel(TestCase):
    """
    This class contains tests for the db post model.
    """

    fixtures = ['test_user.json', 'test_post_type.json', 'test_post.json', 'test_post_address.json', ]

    def setUp(self) -> None:
        self.user: DbUserModel = DbUserModel.objects.get(pk=TEST_USER_PK)
        self.post: DbPostModel = DbPostModel.objects.get(pk=TEST_POST_PK)

    def test_update_post(self):
        """
        Test checks that only allowed fields can be updated.
        """
        new_post_type: DbPostTypeModel = DbPostTypeModel.objects.create(name='another type', description='desc')
        keys_to_update: dict = {
            'name': 'New name',
            'description': 'Updated Description',
            'user': str(uuid.uuid4()),
            'type': new_post_type.id,
        }
        self.post.update_db_record(keys_to_update)

        # check that the attributes of an object have changed
        assert self.post.name == keys_to_update['name']
        assert self.post.description == keys_to_update['description']
        assert self.post.type == new_post_type
        assert self.post.user != keys_to_update['user']

        # check that the DB record has been updated
        updated_post: DbPostModel = DbPostModel.objects.get(id=self.post.id)
        assert updated_post.name == keys_to_update['name']
        assert updated_post.description == keys_to_update['description']
        assert updated_post.type == new_post_type
        assert updated_post.user != keys_to_update['user']
