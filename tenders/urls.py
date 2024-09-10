from django.urls import path

from .views import TenderView, CreateTenderView


urlpatterns = [
    path("", TenderView.as_view()),
    path("new", CreateTenderView.as_view())
]
