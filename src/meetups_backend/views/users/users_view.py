from typing import List

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from meetups_backend.exceptions import UniqueRecordExistsException
from meetups_backend.models import DbUserModel
from meetups_backend.serializers.model_serializers import DbUserModelSerializer
from meetups_backend.serializers.request_serializers import CreateNewUserSerializer, UpdateUserSerializer
from meetups_backend.tools.decorators import request_validation, ensure_existing_record
from meetups_backend.tools.responses import ResponseCreated, ResponseBadRequest, ResponseSuccess


class UsersView(ViewSet):
    """
    This class handles HTTP requests on "/users" endpoints
    """
    serializer_class = DbUserModelSerializer
    db_model_class = DbUserModel

    def get_permissions(self) -> list:
        allow_any_actions: list = ['create']
        permission_classes: list = [AllowAny] if self.action in allow_any_actions else [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @request_validation(CreateNewUserSerializer)
    def create(self, request: Request) -> Response:
        """
        Endpoint that creates a new user.
        """
        email: str = request.data['email']
        password: str = request.data['password']
        bio: str = request.data['bio']

        try:
            new_user: DbUserModel = self.db_model_class.objects.create_user(email, password, bio=bio)
        except UniqueRecordExistsException as e:
            return ResponseBadRequest(message=str(e))
        return ResponseCreated(
            message=f'User with email {email} has been created successfully.',
            created_resource_id=new_user.id
        )

    def list(self, request: Request) -> Response:
        """
        Endpoint that lists all users.
        """
        users: List[DbUserModel] = self.db_model_class.objects.all()
        list_of_users_to_return: list = [self.serializer_class(user).data for user in users]
        return ResponseSuccess(
            message='Users have been listed successfully.',
            response_data={'users': list_of_users_to_return}
        )

    @ensure_existing_record(db_model_class)
    def retrieve(self, request: Request, pk=None) -> Response:
        """
        Endpoint that gets a user by id.
        """
        user: DbUserModel = self.db_model_class.objects.get(id=pk)
        return ResponseSuccess(
            message='User have been retrieved successfully.',
            response_data={'user': self.serializer_class(user).data}
        )

    @request_validation(UpdateUserSerializer)
    @ensure_existing_record(db_model_class)
    def update(self, request: Request, pk=None) -> Response:
        """
        Endpoint that updates a user.
        """
        user_to_update: DbUserModel = self.db_model_class.objects.get(id=pk)
        user_to_update.update_db_record(request.data)
        return ResponseSuccess(message=f'User with id {user_to_update.id} has been updated successfully.')

    @ensure_existing_record(db_model_class)
    def destroy(self, request: Request, pk=None) -> Response:
        """
        Endpoint that deletes a user.
        """
        user_to_delete: DbUserModel = self.db_model_class.objects.get(id=pk)
        user_to_delete.delete()
        return ResponseSuccess(message=f'User with id {pk} has been deleted successfully.')
