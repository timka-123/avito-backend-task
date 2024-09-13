from uuid import uuid4

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import User, Organization, OrganizationResponsible
from .models import Tender, TenderStatus, TenderHistory
from .serializers import TenderFilterSerializer, CreateTenderSerializer, TenderSerializer, MyTenderFilterSerializer, TenderChangeStatusRequest, EditTenderSerializer


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

        responsible = OrganizationResponsible.objects.filter(organization__id=organization.id).filter(user__id=user.id).first()
        if not responsible:
            return Response(
                status=403,
                data={
                    "reason": "You don't have permission to perform this action"
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
            organization = Organization.objects.get(tender.organizationId.id)
            responsible = OrganizationResponsible.objects.filter(organization__id=organization.id).filter(user__id=user.id)
        else:
            return Response(
                status=401,
                data={
                    "reason": "You have not logged in"
                }
            )

        if not responsible:
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
        try:
            tender = Tender.objects.get(tender_id)
        except Tender.DoesNotExist:
            return Response(
                status=404,
                data={
                    "reason": "Tender is not found"
                }
            )

        user = User.objects.filter(username=serializer.validated_data['username']).first()
        organization = Organization.objects.get(tender.organizationId.id)
        responsible = OrganizationResponsible.objects.filter(organization__id=organization.id).filter(user__id=user.id)
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
        if not responsible:
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


class EditTenderView(APIView):
    def patch(self, request: Request, tender_id: str):
        serializer = EditTenderSerializer(request.data)

        if not serializer.is_valid():
            return Response(
                status=400,
                data={
                    "reason": "Bad request"
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

        if request.data.get("serviceType") and request.data.get("serviceType") not in ['Construction', 'Delivery', 'Manufacture']:
            return Response(
                status=400,
                data={
                    "reason": "serviceType field has incorrect value"
                }
            )

        user = User.objects.filter(username=serializer.validated_data['username']).first()
        organization = Organization.objects.get(tender.organizationId.id)
        responsible = OrganizationResponsible.objects.filter(organization__id=organization.id).filter(user__id=user.id)
        if not user:
            return Response(
                status=401,
                data={
                    "reason": "You are not logged in to perform this action"
                }
            )

        if not responsible:
            return Response(
                status=403,
                data={
                    "reason": "You have not permission for perform this action"
                }
            )

        tender_history_item = TenderHistory(
            tender_id=tender_id,
            name=tender.name,
            description=tender.description,
            serviceType=tender.serviceType,
            status=tender.status,
            version=tender.version,
            organizationId=tender.organizationId,
            createdAt=tender.createdAt,
            onwer=tender.owner
        )
        tender_history_item.save()

        for key, value in request.data.items():
            match key:
                case "name": tender.name = value
                case "description": tender.description = value
                case "serviceType": tender.serviceType = value

        tender.version += 1

        tender.save()
        return Response(
            status=200,
            data=TenderSerializer(tender).data
        )


class RollbackTender(APIView):
    def put(self, request: Request, tender_id: str, version: int):
        username = request.query_params.get("username")
        user = User.objects.filter(username=username).first()
        if not username or not user:
            return Response(
                status=401,
                data={
                    "reason": "You have not logged in to perform this action"
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
        organization = Organization.objects.get(tender.organizationId.id)
        responsible = OrganizationResponsible.objects.filter(organization__id=organization.id).filter(user__id=user.id)

        if not responsible:
            return Response(
                status=403,
                data={
                    "reason": "You don't have permission to perform this action"
                }
            )

        try:
            tender_history = TenderHistory.objects.filter(version=version).filter(tender_id=tender_id).first()
        except Exception as e:
            return Response(
                status=400,
                data={
                    "reason": "This tender don't have this version"
                }
            )

        thi = TenderHistory(
            tender_id=tender_id,
            name=tender.name,
            description=tender.description,
            serviceType=tender.serviceType,
            status=tender.status,
            version=tender.version,
            organizationId=tender.organizationId,
            createdAt=tender.createdAt,
            onwer=tender.owner
        )

        tender.name = tender_history.name
        tender.description = tender_history.description
        tender.serviceType = tender_history.serviceType
        tender.status = tender_history.status
        tender.version = tender_history.version
        tender.organizationId = tender_history.organizationId
        tender.createdAt = tender_history.createdAt
        tender.owner = tender_history.owner
        tender.version += 1

        tender.save()

        return Response(
            status=200,
            data=TenderSerializer(tender).data
        )


