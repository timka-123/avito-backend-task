from django.urls import path

from .views import TenderView


urlpatterns = [
    path("", TenderView.as_view())
]
