from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            content=f"You have a new message from {instance.sender.username}."
        )


@receiver(pre_save, sender=Message)
def log_message_edits(sender, instance, **kwargs):
    # Only check for updates to existing messages
    if instance.id:
        try:
            old_instance = Message.objects.get(id=instance.id)
            if old_instance.content != instance.content:
                # Log the old content to history
                MessageHistory.objects.create(
                    message=old_instance,
                    old_content=old_instance.content
                )
                # Mark message as edited
                instance.edited = True
        except Message.DoesNotExist:
            pass 