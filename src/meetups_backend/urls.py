"""
meetups_backend URL Configuration.

In the project, the views are built using the DRF ViewSet class
because its methods like create, list, retrieve etc are
more convenient than Django class based views.
Also, the ViewSet class creates RESTful URLs under the hood
which makes it even more convenient (see DRF docs for reference).

The only limitation: these ViewSets are usually used together
with the DRF router. In order to create complex URLs like
"posts/{post_id}/address/" you need to use a DynamicRoute
class with @action decorator.

This solution seemed quite complex to me and I did not want
to add an unnecessary complexity. So, to create a complex URL
I have decided to use the default Django router and attach ViewSet view to it.
"""
from django.urls import path
from rest_framework.routers import SimpleRouter
import meetups_backend.views as meetups_backend_views


user_router: SimpleRouter = SimpleRouter()
user_router.register(r'users', meetups_backend_views.UsersView, basename='users')

auth_router: SimpleRouter = SimpleRouter()
auth_router.register(r'auth', meetups_backend_views.AuthView, basename='auth')

post_router: SimpleRouter = SimpleRouter()
post_router.register(r'posts', meetups_backend_views.PostsView, basename='posts')


urlpatterns: list = [
    path(
        'posts/<str:pk>/address/',
        meetups_backend_views.PostAddressView.as_view({'put': 'update'}),
        name='post_address_view'
    ),
]
urlpatterns += user_router.urls
urlpatterns += auth_router.urls
urlpatterns += post_router.urls
