from django.urls import path
from .views import Login, Register, UserAddView

app_name = 'account'

urlpatterns = [
    path('login', Login.as_view(), name='login_page'),
    path('register', Register.as_view(), name='register_page'),
    path('api/user/add', UserAddView.as_view(), name='UserAdd_api')
]
