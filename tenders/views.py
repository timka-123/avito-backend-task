from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tender
from .serializers import TenderFilterSerializer


class TenderView(APIView):
    def get(self, request: Request):
        serializer = TenderFilterSerializer(data=request.query_params)
        if not serializer.is_valid() or serializer.validated_data['service_type'] not in ['Construction', 'Delivery',
                                                                                          'Manufacture', ""]:
            return Response(
                status=400,
                data={
                    "reason": "Bad request"
                }
            )

        items = Tender.objects.filter(serviceType=serializer.validated_data['service_type'])[
                serializer.validated_data['offset']:serializer.validated_data['offset'] + serializer.validated_data[
                    'limit']]

        return Response(
            status=200,
            data=items
        )
