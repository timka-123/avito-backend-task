from django.urls import path

from .views import Ping


urlpatterns = [
    path("", Ping.as_view())
]
