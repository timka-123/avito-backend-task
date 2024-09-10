from django.db import models

from core.models import Organization


# Create your models here.


class ServiceTypes(models.TextChoices):
    CONSTRUCTION = "Construction"
    DELIVERY = "Delivery"
    MANUFACTURE = "Manufacture"


class TenderStatus(models.TextChoices):
    CREATED = "Created"
    PUBLISHED = "Published"
    CLOSED = "Closed"


class Tender(models.Model):
    id = models.UUIDField(auto_created=True, primary_key=True, default="uuid_generate_v4()")
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=500, null=False)
    serviceType = models.CharField(choices=ServiceTypes.choices, null=False)
    status = models.CharField(choices=TenderStatus.choices, null=False)
    version = models.IntegerField(default=1, null=False)
    organizationId = models.ForeignKey(Organization, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, null=False)
