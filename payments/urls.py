# Django
from django.urls import path, include

# local
from .views import go_to_gateway_view, callback_gateway_view

# third party
from azbankgateways.urls import az_bank_gateways_urls

urlpatterns = [
    path('bankgateways/', az_bank_gateways_urls()),
    path('go-gateway/<int:package_id>/', go_to_gateway_view, name='go-gateway'),
    path('callback-gateway/', callback_gateway_view, name='callback-gateway')

]
