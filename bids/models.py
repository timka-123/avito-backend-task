from django.db import models

from core.models import User
from tenders.models import Tender


# Create your models here.


class BidStatus(models.TextChoices):
    CREATED = "Created"
    PUBLISHED = "Published"
    CANCELED = "Canceled"
    APPROVED = "Approved"
    DECLINED = "Declined"


class BidAuthorType(models.TextChoices):
    ORGANIZATION = "Organization"
    USER = "User"


class Bid(models.Model):
    id = models.UUIDField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    status = models.CharField(choices=BidStatus.choices, default=BidStatus.PUBLISHED)
    tenderId = models.ForeignKey(Tender, on_delete=models.CASCADE)
    authorType = models.CharField(choices=BidAuthorType.choices)
    authorId = models.ForeignKey(User, on_delete=models.CASCADE)
    version = models.IntegerField(default=1, db_default=1)
    createdAt = models.DateTimeField(auto_now_add=True)
    approved_count = models.IntegerField(default=0, db_default="0")


class BidReview(models.Model):
    id = models.UUIDField(primary_key=True, max_length=100)
    feedback = models.TextField()
    bid_id = models.ForeignKey(Bid, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "bid_reviews"


class BidHistory(models.Model):
    bid_id = models.UUIDField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    status = models.CharField(choices=BidStatus.choices, default=BidStatus.CREATED)
    tenderId = models.ForeignKey(Tender, on_delete=models.CASCADE)
    authorType = models.CharField(choices=BidAuthorType.choices)
    authorId = models.ForeignKey(User, on_delete=models.CASCADE)
    version = models.IntegerField(default=1, db_default=1)
    createdAt = models.DateTimeField(auto_now_add=True)
    approved_count = models.IntegerField(default=0, db_default="0")

    class Meta:
        db_table = "bid_history"
        