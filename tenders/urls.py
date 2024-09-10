from django.urls import path

from .views import TenderView, CreateTenderView, GetMyTenders


urlpatterns = [
    path("", TenderView.as_view()),
    path("new", CreateTenderView.as_view()),
    path("my", GetMyTenders.as_view())
]
