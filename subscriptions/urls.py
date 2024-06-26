# Django
from django.urls import path

# local
from .views import PackageView, PackageDetailView

urlpatterns = [
    path('', PackageView.as_view(), name='package_list'),
    path('<int:package_id>/', PackageDetailView.as_view(), name='package_detail')
]
