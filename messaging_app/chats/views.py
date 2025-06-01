from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating Conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def create(self, request, *args, **kwargs):
        participants_ids = request.data.get('participants', [])
        if not participants_ids:
            return Response(
                {"error": "Participants list is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants_ids)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and sending messages to a conversation.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['timestamp']
    ordering = ['timestamp']  # Default ordering

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        sender_id = request.data.get('sender')
        content = request.data.get('message_body')

        if not conversation_id or not sender_id or not content:
            return Response(
                {"error": "conversation, sender, and message_body are required fields."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            sender = User.objects.get(user_id=sender_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Sender not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            content=content
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)