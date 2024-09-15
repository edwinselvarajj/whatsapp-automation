# from backend.models import 
import datetime
from datetime import timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Count, Sum, Max, Q, Case, When, Value, CharField
from django.db.models import Q, ExpressionWrapper, F, FloatField, Value
from django.db.models.functions import Substr, Coalesce
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import json
import urllib.parse
import time
from urllib.parse import unquote
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from urllib.parse import unquote
from playwright.sync_api import sync_playwright
from backend.whatsapp_session import task_queue, result_queue
import backend.whatsapp_monitor  # Adjust the path based on your project structure
import requests
from django.views.decorators.csrf import csrf_exempt


def send_message_function(contact, message):
    if not contact:
        return None
    
    if not message:
        return None

    task_queue.put({"command": "send_message", "contact": contact, 'message': message})
    result = result_queue.get(timeout=10)  


@api_view(['GET'])
def home_page(request):
    return Response({'message': 'api routes are active'})

@api_view(['GET'])
def login_status(request):
    try:
        # Send task to Playwright worker thread
        task_queue.put({"command": "check_h1"})
        
        # Wait for the result from the worker thread
        result = result_queue.get(timeout=10)  # Timeout if no result in 10 seconds

        if result == 'Chats':
            return Response({"status": "success", "message": "You are on the 'Chats' screen."})
        elif result == 'not found':
            return Response({"status": "error", "message": "h1 element not found"})
        else:
            return Response({"status": "failure", "message": f"Expected 'Chats', but got '{result}'"})

    except Exception as e:
        return Response({"status": "error", "message": str(e)})
    
@api_view(['POST'])
def send_message(request):
    contact = request.data.get('contact')
    message = request.data.get('message')

    try:
        send_message_function(contact, message)
        return Response({"status": "success", "message": 'ok'})

    except Exception as e:
        return Response({"status": "error", "message": str(e)})
