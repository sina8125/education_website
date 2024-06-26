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
    ProfileView
)

profile_urls = [
    path('information/', ProfileView.as_view(), name='information'),
    path('subscriptions/', ProfileSubscriptionView.as_view(), name='subscription'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyCodeView.as_view(), name='verify_code'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', include((profile_urls, 'accounts'), namespace='profile')),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
