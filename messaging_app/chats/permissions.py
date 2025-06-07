# messaging_app/chats/permissions.py

from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Custom permission to allow users to only access their own conversations/messages.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user  # Adjust to match your model's owner field