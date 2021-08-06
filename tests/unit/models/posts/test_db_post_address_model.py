from django.test import TestCase

from meetups_backend.models import DbPostAddressModel
from tests.utils.test_records_pks import TEST_POST_ADDRESS_PK


class TestDbPostAddressModel(TestCase):
    """
    This class contains tests for the db post address model.
    """

    fixtures = ['test_post_address.json', ]

    def setUp(self) -> None:
        self.post_address: DbPostAddressModel = DbPostAddressModel.objects.get(pk=TEST_POST_ADDRESS_PK)

    def test_update_post_address(self):
        """
        Test checks that only allowed fields can be updated.
        """
        keys_to_update: dict = {'country': 'USA', 'house_no': '6', 'floor': '1'}
        self.post_address.update_db_record(keys_to_update)

        # check that the attributes of an object have changed
        assert self.post_address.country == keys_to_update['country']
        assert self.post_address.house_no == keys_to_update['house_no']
        assert self.post_address.floor == keys_to_update['floor']

        # check that the DB record has been updated
        updated_address: DbPostAddressModel = DbPostAddressModel.objects.get(id=self.post_address.id)
        assert updated_address.country == keys_to_update['country']
        assert updated_address.house_no == keys_to_update['house_no']
        assert updated_address.floor == keys_to_update['floor']
