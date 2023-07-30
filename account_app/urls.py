from django.urls import path
from .views import Login, Register

app_name = 'account'

urlpatterns = [
    path('login', Login.as_view(), name='login_page'),
    path('register', Register.as_view(), name='register_page'),
]
