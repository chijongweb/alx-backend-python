import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    # Filter by sender username (exact or contains)
    sender_username = django_filters.CharFilter(field_name="sender__username", lookup_expr='icontains')

    # Filter by conversation participants (username)
    conversation_participant = django_filters.CharFilter(method='filter_by_participant')

    # Filter by timestamp range
    timestamp_after = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    timestamp_before = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    start_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='lte')
    sender = django_filters.CharFilter(field_name="sender__username", lookup_expr='icontains')
    conversation = django_filters.NumberFilter(field_name="conversation__id")
    
    def filter_by_participant(self, queryset, name, value):
        return queryset.filter(conversation__participants__username__icontains=value)

    class Meta:
        model = Message
        fields = ['sender_username', 'conversation_participant', 'timestamp_after', 'timestamp_before']



        

class MessageFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='lte')
    sender = django_filters.CharFilter(field_name="sender__username", lookup_expr='icontains')
    conversation = django_filters.NumberFilter(field_name="conversation__id")

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'start_date', 'end_date']