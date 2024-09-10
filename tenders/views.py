from uuid import uuid4

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User, Organization
from .models import Tender
from .serializers import TenderFilterSerializer, CreateTenderSerializer, TenderSerializer


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

        if serializer.validated_data['service_type']:
            items = TenderSerializer(Tender.objects.filter(serviceType=serializer.validated_data['service_type'])[
                    serializer.validated_data['offset']:serializer.validated_data['offset'] + serializer.validated_data[
                        'limit']], many=True).data
        else:
            items = TenderSerializer(Tender.objects.all()[
                                     serializer.validated_data['offset']:serializer.validated_data['offset'] +
                                                                         serializer.validated_data[
                                                                             'limit']], many=True).data

        return Response(
            status=200,
            data=items
        )


class CreateTenderView(APIView):
    def post(self, request: Request):
        serializer = CreateTenderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=400,
                data={
                    "reason": "Bad request"
                }
            )
        user = User.objects.filter(username=serializer.validated_data['creatorUsername']).first()
        organization = Organization.objects.filter(id__exact=serializer.validated_data['organizationId']).first()
        if not user:
            return Response(
                status=401,
                data={
                    "reason": "User login is not correct or does not exists"
                }
            )
        if not organization:
            return Response(
                status=400,
                data={
                    "reason": "Organization does not exsists"
                }
            )

        tender = Tender.objects.create(
            name=serializer.validated_data['name'],
            description=serializer.validated_data['description'],
            serviceType=serializer.validated_data['serviceType'],
            organizationId_id=serializer.validated_data['organizationId'],
            owner_id=user.id,
            id=uuid4()
        )
        return Response(
            status=200,
            data=TenderSerializer(tender).data
        )
