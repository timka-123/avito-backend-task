from rest_framework.serializers import Serializer, ModelSerializer, IntegerField, CharField

from .models import Bid, BidReview


class CreateBidSerializer(ModelSerializer):
    class Meta:
        model = Bid
        fields = ['name', 'description', 'tenderId', 'authorType', 'authorId']


class BidSerilizer(ModelSerializer):
    class Meta:
        model = Bid
        fields = ['id', 'name', 'status', 'authorType', 'authorId', 'version', 'createdAt']


class MyBidsSerializer(Serializer):
    limit = IntegerField(default=5)
    offset = IntegerField(default=0)
    username = CharField()


class BidReviewSerializer(ModelSerializer):
    class Meta:
        model = BidReview
        fields = ['id', 'description', 'createdAt']


class ListReviewSerializer(Serializer):
    authorUsername = CharField()
    requesterUsername = CharField()
    limit = IntegerField(default=5)
    offset = IntegerField(default=0)
