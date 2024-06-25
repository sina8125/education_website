from azbankgateways.urls import az_bank_gateways_urls
from django.urls import path, include

from .views import go_to_gateway_view, callback_gateway_view

urlpatterns = [
    path('bankgateways/', az_bank_gateways_urls()),
    path('go-gateway/<int:package_id>/', go_to_gateway_view, name='go-gateway'),
    path('callback-gateway/', callback_gateway_view, name='callback-gateway')

]
