from rest_framework.serializers import Serializer, IntegerField, CharField, UUIDField, ModelSerializer

from .models import Tender


class TenderFilterSerializer(Serializer):
    limit = IntegerField(default=5, allow_null=True)
    offset = IntegerField(default=0, allow_null=True)
    service_type = CharField(allow_null=True, default="")


class CreateTenderSerializer(Serializer):
    name = CharField(max_length=100)
    description = CharField(max_length=500)
    serviceType = CharField()
    organizationId = UUIDField()
    creatorUsername = CharField()


class TenderSerializer(ModelSerializer):
    class Meta:
        model = Tender
        fields = ['id', 'name', 'description', 'serviceType', 'status', 'version', 'createdAt']


class MyTenderFilterSerializer(Serializer):
    limit = IntegerField(default=5)
    offset = IntegerField(default=0)
    username = CharField()


class TenderChangeStatusRequest(Serializer):
    status = CharField()
    username = CharField()


class EditTenderSerializer(Serializer):
    name = CharField(max_length=100, allow_null=True, allow_blank=True)
    description = CharField(max_length=500, allow_null=True, allow_blank=True)
    serviceType = CharField(allow_null=True, allow_blank=True)
