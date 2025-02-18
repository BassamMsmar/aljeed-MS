from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend




from .serializers import ShipmentSerializer, ShipmentStatusSerializer
from .models import Shipment, ShipmentStatus
from .filter import ShipmentFilter
from .paginations import ShipmentsPagination





class ShipmentListApi(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShipmentFilter
    pagination_class = ShipmentsPagination


class ShipmentStatusApi(viewsets.ReadOnlyModelViewSet):
    queryset = ShipmentStatus.objects.all()
    serializer_class = ShipmentStatusSerializer



