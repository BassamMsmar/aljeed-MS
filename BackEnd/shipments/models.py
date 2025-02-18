from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

from django.utils.translation import gettext_lazy as _
from project.settings import ALLOWED_HOSTS


from drivers.models import Driver
from customers.models import Customers, Branch
# Create your models here.


class City(models.Model):
    name_ar = models.CharField(_("City Arabic"), max_length=50)
    name_en = models.CharField(_("City English"), max_length=50)

    def __str__(self):
        return self.name_ar


class Stages(models.Model):
    status = models.CharField(_("Status Stages"), max_length=50)

    def __str__(self):
        return self.status


# Create your models here.
class ShipmentStatus(models.Model):
    name_en = models.CharField(_("Status English"), max_length=50)
    name_ar = models.CharField(_("Status Arabic"), max_length=50)

    def __str__(self):
        return self.name_en

    # class Meta:
    #     verbose_name = _("Shipment Status")
    #     verbose_name_plural = _("Shipment Statuses")


class Shipment(models.Model):
    user = models.ForeignKey(
        User,  related_name='shipments_user', on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(
        Driver,  related_name='shipments_driver', on_delete=models.SET_NULL, null=True)
    customer_branch = models.ForeignKey(
        Branch, related_name='shipments_company', on_delete=models.SET_NULL, null=True)
    fare = models.IntegerField(_("Fare"))
    premium = models.IntegerField(_("Premium"), null=True, blank=True)
    fare_return = models.IntegerField(_("Return"), null=True, blank=True)
    code = models.ImageField(blank=True, null=True, upload_to='code')
    days_stayed = models.IntegerField(_("Days Stayed "), null=True, blank=True)
    stay_cost = models.IntegerField(_("Stay Cost"), null=True, blank=True)
    deducted = models.IntegerField(_("Deducted"), null=True, blank=True)
    status = models.ForeignKey(ShipmentStatus, verbose_name=_(
        "Status"), on_delete=models.SET_NULL, null=True, blank=True)
    destination = models.ForeignKey(City, verbose_name=_(
        "Destination"), on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(_("Create At"), default=timezone.now)
    expected_arrival_date = models.DateTimeField(
        _("Expected Arrival Date"), null=True, blank=True, default=timezone.now)
    actual_delivery_date = models.DateTimeField(
        _("Actual Delivery Date "), null=True, blank=True, default=timezone.now)
    notes = models.TextField(_("Notes"), null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.driver} - {self.destination}'

    def save(self, *args, **kwargs):
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=4,
        )
        qr.add_data(f'http://127.0.0.1:8000/shipment/{self.id}/')
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code to image field
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        self.code.save(f'{self.id}_qrcode.png', File(buffer), save=False)

        super().save(*args, **kwargs)
