from django.urls import path
from .views import  UserCreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


user_prefix = 'api/v1/users/'
print (f'{user_prefix}token/')
urlpatterns = [
    path(f'{user_prefix}', UserCreateAPIView.as_view(), name='user_create'),
    path(f'{user_prefix}token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'{user_prefix}token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]