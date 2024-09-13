import uuid

from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, default="uuid_generate_v4()")
    username = models.CharField(max_length=50, unique=True, null=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "employee"


class OrganizationType(models.TextChoices):
    IE = 'IE'
    LLC = 'LLC'
    JSC = 'JSC'


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default="uuid_generate_v4()")
    name = models.CharField(max_length=100, null=False)
    description = models.TextField()
    type = models.CharField(choices=OrganizationType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'organization'


class OrganizationResponsible(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='responsibles')
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = "organization_responsible"
