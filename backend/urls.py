 
from . import views
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('login-status', views.login_status, name='login_status'),
    path('send-message', views.send_message, name='send_message'),
    path('global-search', views.send_message, name='global_search')

]