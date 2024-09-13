from django.urls import path

from .views import NewBid, MyBids, ListTenderBids

urlpatterns = [
    path("new", NewBid.as_view()),
    path("my", MyBids.as_view()),
    path("<int:tender_id>/list", ListTenderBids.as_view()),
]

