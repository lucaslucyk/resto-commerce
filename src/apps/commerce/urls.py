### django
from django.urls import path, include

### own
from apps.commerce import views


urlpatterns = [
    path('checkout/<int:order>/', views.checkout, name='checkout'),
    path('mp-callback/<int:order>/', views.mp_callback, name='mp_callback'),
]
