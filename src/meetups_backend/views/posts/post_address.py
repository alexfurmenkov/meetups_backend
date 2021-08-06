from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from meetups_backend.models import DbPostModel, DbPostAddressModel
from meetups_backend.serializers.request_serializers.posts import UpdatePostAddressSerializer
from meetups_backend.tools.decorators import request_validation, ensure_existing_record
from meetups_backend.tools.responses import ResponseSuccess


class PostAddressView(ViewSet):
    """
    This class handles HTTP requests on "/posts/{post_id}/address/" endpoints
    """

    def get_permissions(self) -> list:
        permission_classes: list = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @request_validation(UpdatePostAddressSerializer)
    @ensure_existing_record(DbPostModel)
    def update(self, request: Request, pk=None) -> Response:
        """
        Endpoint that updates details of a post with the given id.
        """
        # update address of the post
        post: DbPostModel = DbPostModel.objects.get(user=request.user, id=pk)
        post_address_to_update: DbPostAddressModel = post.address
        post_address_to_update.update_db_record(request.data)

        # return successful response
        return ResponseSuccess(message=f'Address of a post with id {pk} has been updated successfully.')
