from uuid import uuid4

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User, Organization
from .models import Tender, TenderStatus
from .serializers import TenderFilterSerializer, CreateTenderSerializer, TenderSerializer, MyTenderFilterSerializer, TenderChangeStatusRequest


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
            items = TenderSerializer(Tender.objects.filter(serviceType=serializer.validated_data['service_type']).filter(status="Published")[
                    serializer.validated_data['offset']:serializer.validated_data['offset'] + serializer.validated_data[
                        'limit']], many=True).data
        else:
            items = TenderSerializer(Tender.objects.filter(status="Published")[
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
                    "reason": "Organization does not exists"
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


class GetMyTenders(APIView):
    def get(self, request: Request):
        serializer = MyTenderFilterSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                status=400,
                data={
                    "reason": "Bad request"
                }
            )

        user = User.objects.filter(username=serializer.validated_data['username']).first()
        if not user:
            return Response(
                status=401,
                data={
                    "reason": "User does not exists"
                }
            )

        return Response(
            status=200,
            data=TenderSerializer(
                Tender.objects.filter(owner__username=serializer.validated_data['username']).all()[
                                     serializer.validated_data['offset']:serializer.validated_data['offset'] +
                                                                         serializer.validated_data[
                                                                             'limit']],
                many=True
            ).data
        )


class TenderStatusView(APIView):
    def get(self, request: Request, tender_id: str):
        try:
            tender = Tender.objects.get(tender_id)
        except Tender.DoesNotExist:
            return Response(
                status=404,
                data={
                    "reason": "Tender is not found"
                }
            )
        if request.query_params.get("username"):
            user = User.objects.filter(username=request.query_params.get("username")).first()
        else:
            return Response(
                status=401,
                data={
                    "reason": "You have not logged in"
                }
            )

        if not user or user.id != tender.owner:
            return Response(
                status=403,
                data={
                    "reason": "You have not permission to view this resource"
                }
            )

        return Response(
            status=200,
            data=tender.status
        )

    def patch(self, request: Request, tender_id: str):
        serializer = TenderFilterSerializer(data=request.data)
        if not serializer.is_valid() or serializer.validated_data['status'] not in ['Created', 'Published', 'Closed']:
            return Response(
                status=400,
                data={
                    "reason": "Bad request"
                }
            )

        user = User.objects.filter(username=serializer.validated_data['username']).first()
        if not user:
            return Response(
                status=401,
                data={
                    "reason": "You are not logged in to perform this action"
                }
            )

        try:
            tender = Tender.objects.get(tender_id)
        except Tender.DoesNotExist:
            return Response(
                status=404,
                data={
                    "reason": "Tender is not found"
                }
            )
        if tender.owner_id != user.id:
            return Response(
                status=403,
                data={
                    "reason": "You have not permission for perform this action"
                }
            )

        tender.status = serializer.validated_data['status']
        tender.save()

        return Response(
            status=200,
            data=TenderSerializer(tender).data
        )
