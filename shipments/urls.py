from django.urls import path, include
from .views import ShipmentList, ShipmentsDetail,  ShipmentCreateView, waybill, change_stutus
from .api import ShipmentListApi
from .send_sms import send_sms

from rest_framework import routers

from shipments import api
router = routers.DefaultRouter()
router.register('', api.ShipmentListApi)




urlpatterns = [
    path('<str:status>', ShipmentList.as_view(), name='shipment_list'),
    path('<int:pk>/', ShipmentsDetail.as_view(), name='shipment_detail'),
    path('change_stutus/<int:pk>/', change_stutus, name='change_stutus'),
    path('change_stutus_detail/<int:pk>/', change_stutus, name='change_stutus_detail'),
    path('waybill/<int:pk>/', waybill.as_view(), name='waybill_detail'),
    path('create/', ShipmentCreateView.as_view(), name='shipment_create'),

    path("send_sms/<str:status>", send_sms, name="send_sms"),

    #api
    path('api/list', include(router.urls), name='shipment_list_api')

] 