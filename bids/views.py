from uuid import uuid4

from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Bid
from core.models import User
from tenders.models import Tender
from .serializer import CreateBidSerializer, BidSerilizer, MyBidsSerializer


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
    def get(self, request: Request):
        serializer = MyBidsSerializer(request.query_params)
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
                    "reason": "You are not logged in to perform this action"
                }
            )

        bids = Bid.objects.filter(authorId__id=user.id).all()
        return Response(
            status=200,
            data=BidSerilizer(bids, many=True).data
        )


class ListTenderBids(APIView):
    def get(self, request: Request, tender_id: str):
        serializer = MyBidsSerializer(request.query_params)
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
        bids = Bid.objects.filter(tenderId__id=tender_id).all()
        return Response(
            status=200,
            data=BidSerilizer(bids, many=True).data
        )
