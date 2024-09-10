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


class OrganizationType(models.Model):
    IE = 'IE'
    LLC = 'LLC'
    JSC = 'JSC'

    class Meta:
        db_table = "organization_type"


class Organization(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default="uuid_generate_v4()")
    name = models.CharField(max_length=100, null=False)
    description = models.TextField()
    organization_type = models.ForeignKey(OrganizationType, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'organization'
