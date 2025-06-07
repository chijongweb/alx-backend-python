# messaging_app/chats/permissions.py

from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to:
    - Allow only authenticated users
    - Allow only participants of a conversation to interact with messages
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Called for detail views (e.g. update, delete).
        Assumes `obj.conversation` has a ManyToMany relation like `participants`.
        """
        return request.user in obj.conversation.participants.all()