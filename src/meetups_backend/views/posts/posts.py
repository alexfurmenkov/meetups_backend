from typing import List

from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from meetups_backend.models import DbPostAddressModel, DbPostModel, DbPostTypeModel
from meetups_backend.serializers.request_serializers import CreateNewPostSerializer
from meetups_backend.serializers.model_serializers import DbPostModelSerializer
from meetups_backend.serializers.request_serializers.posts import UpdatePostSerializer
from meetups_backend.tools.decorators import request_validation, ensure_existing_record
from meetups_backend.tools.responses import ResponseCreated, ResponseSuccess


class PostsView(ViewSet):
    """
    This class handles HTTP requests on "/posts/" endpoints
    """
    serializer_class = DbPostModelSerializer
    db_model_class = DbPostModel

    def get_permissions(self) -> list:
        permission_classes: list = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @request_validation(CreateNewPostSerializer)
    def create(self, request: Request) -> Response:
        """
        Endpoint that creates a new post.
        """
        address_details: dict = request.data['address']
        post_details: dict = request.data['post_details']

        # create new post address record
        post_address: DbPostAddressModel = DbPostAddressModel.objects.create(**address_details)

        # create new post record
        type_id: str = post_details.pop('type')
        post_type: DbPostTypeModel = DbPostTypeModel.objects.get(id=type_id)
        new_post: DbPostModel = self.db_model_class.objects.create(
            user=request.user,
            type=post_type,
            address=post_address,
            **post_details
        )

        # return response with new post id
        return ResponseCreated(message='New post has been successfully created.', created_resource_id=new_post.id)

    def list(self, request: Request) -> Response:
        """
        Endpoint that lists all posts of a certain user.
        """
        # find all posts of the user from request
        user_posts: List[DbPostModel] = self.db_model_class.objects.filter(user=request.user)
        # serialize the posts
        serializer = self.serializer_class(user_posts, many=True)
        # return a response
        return ResponseSuccess(message='Posts have been listed successfully.', response_data={'posts': serializer.data})

    @ensure_existing_record(db_model_class)
    def retrieve(self, request: Request, pk=None) -> Response:
        """
        Endpoint that gets a user post by id.
        """
        # find post of the user from request with the given id
        user_post: DbPostModel = self.db_model_class.objects.get(user=request.user, id=pk)
        # serialize the post
        serializer = self.serializer_class(user_post)
        # return a response
        return ResponseSuccess(
            message='Post have been retrieved successfully.',
            response_data={'post': serializer.data}
        )

    @request_validation(UpdatePostSerializer)
    @ensure_existing_record(db_model_class)
    def update(self, request: Request, pk=None) -> Response:
        """
        Endpoint that updates details of a post with the given id.
        """
        # update the post
        post_to_update: DbPostModel = self.db_model_class.objects.get(user=request.user, id=pk)
        post_to_update.update_db_record(request.data)

        # return successful response
        return ResponseSuccess(message=f'Post with id {pk} has been updated successfully.')

    @ensure_existing_record(db_model_class)
    def destroy(self, request: Request, pk=None) -> Response:
        """
        Endpoint that deletes a post.
        """
        # delete the post
        post_to_delete: DbPostModel = self.db_model_class.objects.get(user=request.user, id=pk)
        post_to_delete.delete()

        # return successful response
        return ResponseSuccess(message=f'Post with id {pk} has been deleted successfully.')
