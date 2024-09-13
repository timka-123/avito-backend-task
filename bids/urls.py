from django.urls import path

from .views import NewBid, MyBids, ListTenderBids, BidStatusView, BidReviewView, EditBid, RollbackBid, SubmitFeedback

urlpatterns = [
    path("new", NewBid.as_view()),
    path("my", MyBids.as_view()),
    path("<int:tender_id>/list", ListTenderBids.as_view()),
    path("<int:bid_id>/status", BidStatusView.as_view()),
    path("<int:bid_id>/edit", EditBid.as_view()),
    path("<int:bid_id>/submit_decision", SubmitFeedback.as_view()),
    path("<int:bid_id>/rollback/<int:version>", RollbackBid.as_view()),
    path("<int:bid_id>/feedback", BidReviewView.as_view())
]

