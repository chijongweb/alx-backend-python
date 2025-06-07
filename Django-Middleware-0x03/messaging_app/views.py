from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Simple view for test
def sample_view(request):
    return HttpResponse("This is the messaging app home.")

# Example API view: get or post messages (in-memory for now)
messages = []  # Simulated in-memory storage

@csrf_exempt
def messages_view(request):
    if request.method == 'GET':
        return JsonResponse({'messages': messages})

    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            text = data.get('text')
            if text:
                messages.append({'id': len(messages) + 1, 'text': text})
                return JsonResponse({'message': 'Message added successfully'}, status=201)
            else:
                return JsonResponse({'error': 'Missing "text" in request body'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)