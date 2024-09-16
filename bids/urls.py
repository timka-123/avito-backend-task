from django.urls import path

from .views import NewBid, MyBids, ListTenderBids, BidStatusView, BidReviewView, EditBid, RollbackBid, SubmitFeedback, ViewFeedbacks

urlpatterns = [
    path("new", NewBid.as_view()),
    path("my", MyBids.as_view()),
    path("<str:tender_id>/list", ListTenderBids.as_view()),
    path("<str:bid_id>/status", BidStatusView.as_view()),
    path("<str:bid_id>/edit", EditBid.as_view()),
    path("<str:bid_id>/submit_decision", SubmitFeedback.as_view()),
    path("<str:bid_id>/rollback/<int:version>", RollbackBid.as_view()),
    path("<str:bid_id>/feedback", BidReviewView.as_view()),
    path("<str:tender_id>/reviews", ViewFeedbacks.as_view())
]

