from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from core.models import User


class UsernamePermission(BasePermission):
    def has_permission(self, request: Request, view):
        username = request.query_params.get("username")
        if not username:
            return False
        user = User.objects.filter(username=username).first()
        if not user:
            return False
        return True
