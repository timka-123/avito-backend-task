from rest_framework.serializers import Serializer, IntegerField, CharField


class TenderFilterSerializer(Serializer):
    limit = IntegerField(default=5, allow_null=True)
    offset = IntegerField(default=0, allow_null=True)
    service_type = CharField(allow_null=True, default="")
