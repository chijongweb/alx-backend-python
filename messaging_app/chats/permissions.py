# messaging_app/chats/permissions.py

from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow users to access their own messages/conversations.
    """

    def has_object_permission(self, request, view, obj):
        # Replace `obj.user` with the correct ownership field
        return obj.user == request.user