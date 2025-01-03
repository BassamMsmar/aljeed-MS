from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from .models import Shipment, ShipmentStatus
from django.db.models import Value

from datetime import datetime
from django.utils import timezone


from receipt.models import Receipt
# Create your views here.


class ShipmentList(ListView):
    model = Shipment

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_date = timezone.now()

        # date_1 = timezone.now()
        for shipment in context['object_list']:
            date_created = shipment.created_at
            days_since_creation = (current_date - date_created).days

            shipment.days_since_creation = days_since_creation

        return context

    def get_queryset(self):
        # Get the status from the URL parameter, or default to 'All' if not provided
        status_name = self.kwargs.get('status', 'All')

        if status_name == 'All':
            # If 'All' is selected, return all shipments
            return Shipment.objects.all()
        else:
            try:
                # Get the ShipmentStatus object corresponding to the status name
                shipment_status = ShipmentStatus.objects.get(name_en=status_name)
                # Filter shipments based on the selected status
                return Shipment.objects.filter(status=shipment_status)
            except ShipmentStatus.DoesNotExist:
                # If the status does not exist, return an empty queryset or handle it accordingly
                return Shipment.objects.none()


class ShipmentsDetail(UpdateView):
    model = Shipment
    template_name = 'shipments/shipment_detail.html'
    fields = ['driver', 'customer_branch', 'fare', 'days_stayed', 'stay_cost', 'deducted',
              'status', 'destination', 'expected_arrival_date', 'actual_delivery_date']

    def get_queryset(self):
        # Get the queryset of shipments
        queryset = super().get_queryset()

        for shipment in queryset:
            date_1 = timezone.now()
            date_2 = shipment.created_at
            difference = date_1 - date_2

        queryset = queryset.annotate(
            days_since_creation=Value(difference.days))

        return queryset

    def get_success_url(self):
        return reverse('shipment_detail', kwargs={'pk': self.object.pk})


class waybill(DetailView):
    model = Shipment
    template_name = 'shipments/waybill.html'


class ShipmentCreateView(CreateView):
    model = Shipment
    fields = ['driver', 'customer_branch', 'fare', 'premium',
              'status', 'destination', 'expected_arrival_date']

    def form_valid(self, form):
        # تعيين المستخدم الحالي إلى حقل "user" في الشحنة
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('shipment_list', kwargs={'status': 'All'})


def change_stutus(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)
    if shipment.status == 'Recieved':
        shipment.status = 'Processed'

    elif shipment.status == 'Processed':
        shipment.status = 'Shipped'

    elif shipment.status == 'Processed':
        shipment.status = 'Shipped'

    elif shipment.status == 'Shipped':
        shipment.status = 'Delivered'

    elif shipment.status == 'Delivered':
        shipment.status = 'Feedback'

    elif shipment.status == 'Feedback':
        shipment.status = 'Completed'

    shipment.save()
    return redirect('shipment_list', status='All')


def change_stutus_detail(request, pk):
    shipment = get_object_or_404(Shipment, pk=pk)
    if shipment.status == 'Recieved':
        shipment.status = 'Processed'

    elif shipment.status == 'Processed':
        shipment.status = 'Shipped'

    elif shipment.status == 'Processed':
        shipment.status = 'Shipped'

    elif shipment.status == 'Shipped':
        shipment.status = 'Delivered'

    elif shipment.status == 'Delivered':
        shipment.status = 'Feedback'

    elif shipment.status == 'Feedback':
        shipment.status = 'Completed'

    shipment.save()
    return redirect(f'shipment_detail/{{self.pk}}')
