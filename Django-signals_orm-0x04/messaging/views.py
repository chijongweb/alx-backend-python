from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Message
from .forms import MessageForm  # Ensure this form exists


@login_required
def delete_user(request):
    """Logs out and deletes the current logged-in user."""
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')


@login_required
def send_message(request, receiver_id):
    """Send a message from the logged-in user to the specified receiver."""
    receiver = get_object_or_404(User, id=receiver_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            # Assign sender as current user here:
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('inbox')
    else:
        form = MessageForm()
    
    return render(request, 'messaging/send_message.html', {'form': form, 'receiver': receiver})


@login_required
def inbox(request):
    """
    Display inbox messages where the logged-in user is the receiver,
    including threaded replies, optimized with select_related and prefetch_related.
    """
    messages = (
        Message.objects.filter(receiver=request.user, parent_message__isnull=True)
        .select_related('sender', 'receiver')
        .prefetch_related('replies__sender', 'replies__receiver')
    )
    return render(request, 'messaging/inbox.html', {'messages': messages})