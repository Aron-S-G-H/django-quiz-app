from rest_framework import serializers
from django.contrib.auth.models import User
from django import forms


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'first_name': {'required': True}, 'last_name': {'required': True}, 'email': {'required': True}}
