from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from meetups_backend.serializers.request_serializers import LoginSerializer
from meetups_backend.tools.decorators import request_validation
from meetups_backend.tools.auth_system_class import AuthSystem
from meetups_backend.tools.responses import ResponseNotFound, ResponseSuccess


class AuthView(ViewSet):
    """
    Class that handles requests to "/auth" endpoints.
    """
    def get_permissions(self) -> list:
        allow_any_actions: list = ['login']
        permission_classes: list = [AllowAny] if self.action in allow_any_actions else [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @request_validation(LoginSerializer)
    @action(detail=False, methods=['post'])
    def login(self, request: Request) -> Response:
        """
        Endpoint that logs user in.
        Updates last login and generates a JWT token.
        """
        # authenticate a user using AuthSystem class
        email: str = request.data['email']
        password: str = request.data['password']
        auth_obj: AuthSystem = AuthSystem.authenticate_user(email, password)

        # if cannot authenticate -> return 404 Response
        if not auth_obj:
            return ResponseNotFound(message='User with given credentials is not found.')

        # generate JWT token and update last login
        auth_obj.update_last_login_date()
        jwt_token: str = auth_obj.jwt_token()
        return ResponseSuccess(message='Login is successful.', response_data={'auth_token': jwt_token})
