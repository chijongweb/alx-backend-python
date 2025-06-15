from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from .models import Message
from .forms import MessageForm  # Ensure this form exists


@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Log out before deleting the user
    user.delete()    # Delete the user and cascade related data
    return redirect('home')  # Redirect to homepage or landing page


@login_required
def send_message(request, receiver_id):
    receiver = get_object_or_404(User, id=receiver_id)

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = receiver
            msg.save()
            return redirect('inbox')
    else:
        form = MessageForm()

    return render(request, 'messaging/send_message.html', {'form': form, 'receiver': receiver})


@login_required
def inbox(request):
    messages = Message.objects.filter(receiver=request.user, parent_message__isnull=True) \
        .select_related('sender', 'receiver') \
        .prefetch_related('replies__sender', 'replies__receiver')

    return render(request, 'messaging/inbox.html', {'messages': messages})