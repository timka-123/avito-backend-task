from django.db import models

from core.models import Organization, User


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
    id = models.UUIDField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=500, null=False)
    serviceType = models.CharField(choices=ServiceTypes.choices, null=False)
    status = models.CharField(choices=TenderStatus.choices, null=False, default=TenderStatus.CREATED)
    version = models.IntegerField(default=1, null=False)
    organizationId = models.ForeignKey(Organization, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, null=False)


class TenderHistory(models.Model):
    tender_id = models.UUIDField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(max_length=500, null=False)
    serviceType = models.CharField(choices=ServiceTypes.choices, null=False)
    status = models.CharField(choices=TenderStatus.choices, null=False, default=TenderStatus.CREATED)
    version = models.IntegerField(default=1, null=False)
    organizationId = models.ForeignKey(Organization, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True, null=False)
