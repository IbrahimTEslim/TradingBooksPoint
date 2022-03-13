from django.urls import path,include
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenVerifyView
from .api import RegisterApi
from .views import ChangePasswordView,ConfirmationEmail,ConfirmUser

urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('refresh/',jwt_views.TokenRefreshView.as_view(), name='refresh'),
    path('register/', RegisterApi.as_view(), name='register'),
    path('apiv/', TokenVerifyView.as_view(), name='token_verify'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('email_confirmation/confirm/',ConfirmUser.as_view(),name='user_confirmation'),
    path('email_confirmation/',ConfirmationEmail.as_view(),name='email_confirmation'),

]