# Django
from django.urls import path, include

# local
from .views import (
    RegisterView,
    VerifyCodeView,
    LoginView,
    ChangePasswordView,
    ProfileSubscriptionView,
    UserLogoutView,
    ProfileView,
    LoginAPIView,
    RefreshTokenView,
    RegisterAPIView,
    VerifyCodeAPIView
)

# third party
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

profile_urls = [
    path('information/', ProfileView.as_view(), name='information'),
    path('subscriptions/', ProfileSubscriptionView.as_view(), name='subscription'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]

api_urls = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('login/', LoginAPIView.as_view(), name='login_api'),
    path('register/', RegisterAPIView.as_view(), name='register_api'),
    path('verify/', VerifyCodeAPIView.as_view(), name='verify_code'),
]

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyCodeView.as_view(), name='verify_code'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', include((profile_urls, 'accounts'), namespace='profile')),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('api/', include((api_urls,'accounts'), namespace='account_api'))
]
