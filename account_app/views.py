from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from quiz_app.permissions import IsStaff
from .forms import LoginForm, RegisterForm
from .serializers import UserSerializer


class Login(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('quiz:quiz_page')
        else:
            form = LoginForm()
            return render(request, 'account_app/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['fullname'], password=cd['password'])

            if user is not None:
                login(request, user, backend="django.contrib.auth.backends.ModelBackend")
                return redirect('quiz:quiz_page')
            else:
                form.add_error('fullname', 'Invalid User Data')

        return render(request, 'account_app/login.html', {'form': form})


class Register(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('quiz:quiz_page')
        else:
            form = RegisterForm()
            return render(request, 'account_app/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            fullname = f"{cd['first_name']} {cd['last_name']}"
            user = User.objects.create_user(
                username=fullname,
                first_name=cd['first_name'],
                last_name=cd['last_name'],
                email=cd['email'],
                password=cd['password'],
            )
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")
            return redirect('quiz:quiz_page')
        return render(request, 'account_app/register.html', {'form': form})


# ----------------- API VIEWS--------------------


class UserAddView(APIView):
    permission_classes = [IsAuthenticated, IsStaff]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"response": request.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

