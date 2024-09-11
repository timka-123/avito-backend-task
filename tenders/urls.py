from django.urls import path

from .views import TenderView, CreateTenderView, GetMyTenders, TenderStatusView, EditTenderView, RollbackTender


urlpatterns = [
    path("", TenderView.as_view()),
    path("new", CreateTenderView.as_view()),
    path("my", GetMyTenders.as_view()),
    path("<int:tender_id>/status", TenderStatusView.as_view()),
    path("<int:tender_id>/edit", EditTenderView.as_view()),
    path("<int:tender_id>/rollback/<int:version>", RollbackTender.as_view())
]
