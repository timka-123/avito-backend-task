from uuid import uuid4

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Bid, BidHistory, BidStatus, BidReview
from core.models import User, Organization, OrganizationResponsible
from tenders.models import Tender, TenderStatus
from .serializer import CreateBidSerializer, BidSerilizer, MyBidsSerializer, ListReviewSerializer, BidReviewSerializer
from .permissions import UsernamePermission


class NewBid(APIView):
    def post(self, request: Request):
        serializer = CreateBidSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                status=400,
                data={
                    "reason": "Bad request"
                }
            )
        serializer.validated_data['id'] = uuid4()
        bid: Bid = serializer.create(serializer.validated_data)

        return Response(
            status=200,
            data=BidSerilizer(bid).data
        )


class MyBids(APIView):
    permission_classes = [UsernamePermission]

    def get(self, request: Request):
        serializer = MyBidsSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                status=400,
                data={
                    "reason": "Bad request"
                }
            )

        bids = Bid.objects.filter(authorId__username=serializer.validated_data['username']).all()
        return Response(
            status=200,
            data=BidSerilizer(bids, many=True).data
        )


class ListTenderBids(APIView):
    permission_classes = [UsernamePermission]

    def get(self, request: Request, tender_id: str):
        serializer = MyBidsSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                status=400,
                data={
                    "reason": "Bad request"
                }
            )
        try:
            Tender.objects.get(id=tender_id)
        except Tender.DoesNotExist:
            return Response(
                status=404,
                data={
                    "reason": "Tender is not found"
                }
            )
        bids = Bid.objects.filter(tenderId__id=tender_id).all()
        return Response(
            data=BidSerilizer(bids, many=True).data
        )


class BidStatusView(APIView):
    permission_classes = [UsernamePermission]

    def get(self, request: Request, bid_id: str):
        try:
            bid = Bid.objects.get(id=bid_id)
        except Bid.DoesNotExist:
            return Response(
                status=404,
                data={
                    "reason": "Bid is not found"
                }
            )

        user = User.objects.filter(username=request.query_params.get("username")).first()

        tender = bid.tenderId
        organization = tender.organizationId
        responsible = OrganizationResponsible.objects.filter(organization__id=organization.id).filter(user__id=user.id)
        if not responsible and user != bid.authorId:
            return Response(
                status=403,
                data={
                    "reason": "You don't have permission to view this resource"
                }
            )

        return Response(
            data=bid.status
        )

    def put(self, request: Request, bid_id: str):
        status = request.query_params.get("status")
        if not status or status not in ['Created', 'Published', 'Canceled']:
            return Response(
                status=400,
                data={
                    "reason": "Bad request"
                }
            )
        try:
            bid = Bid.objects.get(id=bid_id)
        except Bid.DoesNotExist:
            return Response(
                status=404,
                data={
                    "reason": "Bid is not found"
                }
            )

        user = User.objects.filter(username=request.query_params.get("username")).first()

        organization = bid.tenderId.organizationId
        responsible = OrganizationResponsible.objects.filter(organization__id=organization.id).filter(user__id=user.id)
        if not responsible and user != bid.authorId:
            return Response(
                status=403,
                data={
                    "reason": "You don't have permission to edit this resource"
                }
            )


        bid.status = status
        bid.save()
        return Response(
            data=BidSerilizer(bid).data
        )


class EditBid(APIView):
    permission_classes = [UsernamePermission]

    def patch(self, request: Request, bid_id: str):
        username = request.query_params.get("username")
        try:
            bid = Bid.objects.get(id=bid_id)
        except Bid.DoesNotExist:
            return Response(
                status=404,
                data={
                    "reason": "Bid is not found"
                }
            )

        user = User.objects.filter(username=username).first()

        organization = bid.tenderId.organizationId
        responsible = OrganizationResponsible.objects.filter(organization__id=organization.id).filter(user__id=user.id)
        if not responsible and user != bid.authorId:
            return Response(
                status=403,
                data={
                    "reason": "You don't have permission to edit this resource"
                }
            )

        BidHistory.objects.create(
            bid_id=bid_id,
            name=bid.name,
            description=bid.description,
            status=bid.status,
            tenderId=bid.tenderId,
            authorId=bid.authorId,
            authorType=bid.authorType,
            version=bid.version,
            createdAt=bid.createdAt,
            id=str(uuid4())
        )

        for key, value in request.data.items():
            match key:
                case "name": bid.name = value
                case "description": bid.description = value

        bid.version += 1
        bid.save()
        return Response(
            data=BidSerilizer(bid).data
        )


class RollbackBid(APIView):
    permission_classes = [UsernamePermission]

    def put(self, request: Request, bid_id: str, version: int):
        username = request.query_params.get("username")
        try:
            bid = Bid.objects.get(id=bid_id)
        except Bid.DoesNotExist:
            return Response(
                status=404,
                data={
                    "reason": "Bid is not found"
                }
            )
        if bid.authorId.username != username:
            return Response(
                status=403,
                data={
                    "reason": "You have not permission to edit this resource"
                }
            )
        try:
            bid_history = BidHistory.objects.filter(version=version).filter(bid_id=bid.id).first()
        except Exception as e:
            return Response(
                status=400,
                data={
                    "reason": "This bid don't have this version"
                }
            )
        if not bid_history:
            return Response(
                status=400,
                data={
                    "reason": "This bid don't have this version"
                }
            )
        BidHistory.objects.create(
            bid_id=bid_id,
            name=bid.name,
            description=bid.description,
            status=bid.status,
            tenderId=bid.tenderId,
            authorId=bid.authorId,
            authorType=bid.authorType,
            version=bid.version,
            createdAt=bid.createdAt,
            id=str(uuid4())
        )
        bid.version += 1
        bid.name = bid_history.name
        bid.description = bid_history.description
        bid.status = bid_history.status
        bid.tenderId = bid_history.tenderId
        bid.authorId = bid_history.authorId
        bid.authorType = bid_history.authorType
        bid.authorType = bid_history.authorType
        bid.createdAt = bid_history.createdAt

        bid.save()

        return Response(
            data=BidSerilizer(bid).data
        )


class SubmitFeedback(APIView):
    permission_classes = [UsernamePermission]

    def put(self, request: Request, bid_id: str):
        username = request.query_params.get("username")
        user = User.objects.filter(username=username).first()
        decision = request.query_params.get("decision")
        if not decision:
            return Response(
                status=400,
                data={
                    "reason": "Bad request"
                }
            )
        try:
            bid = Bid.objects.get(id=bid_id)
        except Bid.DoesNotExist:
            return Response(
                status=404,
                data={
                    "reason": "Bid is not found"
                }
            )

        organization = bid.tenderId.organizationId
        responsible = OrganizationResponsible.objects.filter(organization__id=organization.id).filter(user__id=user.id)
        if not responsible:
            return Response(
                status=403,
                data={
                    "reason": "You don't have permission to edit this resource"
                }
            )

        if decision == "Rejected":
            bid.status = BidStatus.DECLINED
            bid.save()
        else:
            bid.approved_count += 1
            people_count = OrganizationResponsible.objects.filter(organization__id=organization.id).count()
            if min(3, people_count) >= bid.approved_count:
                bid.tenderId.status = TenderStatus.CLOSED
                bid.tenderId.save()
                bid.status = BidStatus.APPROVED
            bid.save()

        return Response(
            data=BidSerilizer(bid).data
        )


class BidReviewView(APIView):
    permission_classes = [UsernamePermission]

    def put(self, request: Request, bid_id: str):
        feedback = request.query_params.get("bidFeedback")
        username = request.query_params.get("username")
        user = User.objects.filter(username=username).first()
        bid = Bid.objects.get(id=bid_id)
        organization = bid.tenderId.organizationId
        responsible = OrganizationResponsible.objects.filter(organization__id=organization.id).filter(user__id=user.id)
        if not feedback:
            return Response(
                status=400,
                data={
                    "reason": "Feedback field is required"
                }
            )

        if not responsible:
            return Response(
                status=403,
                data={
                    "reason": "You don't have permission to send description to this resource"
                }
            )

        BidReview.objects.create(
            id=uuid4(),
            description=feedback,
            bid_id=bid.id,
            user_id=user.id
        )
        return Response(
            data=BidSerilizer(bid).data
        )


class ViewFeedbacks(APIView):
    def get(self, request: Request, tender_id: str):
        serializer = ListReviewSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(
                status=400,
                data={
                    "reason": "Bad request"
                }
            )

        try:
            tender = Tender.objects.get(id=tender_id)
        except Tender.DoesNotExist:
            return Response(
                status=404,
                data={
                    "reason": "Tender is not found"
                }
            )

        requester = User.objects.filter(username=serializer.validated_data['requesterUsername']).first()
        author = User.objects.filter(username=serializer.validated_data['authorUsername']).first()
        if not requester:
            return Response(
                status=401,
                data={
                    "reason": "You must to login"
                }
            )

        if not author:
            return Response(
                status=400,
                data={
                    "reason": "Bad request"
                }
            )

        bid = Bid.objects.filter(tenderId__id=tender_id).filter(authorId=author).first()
        if not bid:
            return Response(
                status=400,
                data={
                    "reason": "This author has not applied to this tender"
                }
            )
        organization = bid.tenderId.organizationId
        responsible = OrganizationResponsible.objects.filter(organization__id=organization.id).filter(user__id=requester.id)
        if not responsible:
            return Response(
                status=403,
                data={
                    "reason": "You have not permission to view this resource"
                }
            )

        reviews = BidReview.objects.filter(bid=bid).all()[
                    serializer.validated_data['offset']:serializer.validated_data['offset'] + serializer.validated_data[
                        'limit']]

        return Response(
            data=BidReviewSerializer(reviews, many=True).data
        )
