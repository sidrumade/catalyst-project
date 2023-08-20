from rest_framework import serializers
from .models import Company
from django.contrib.auth.models import User
from rest_framework.serializers import Serializer, ModelSerializer
from allauth.account.models import EmailAddress


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["name","industry", "size_range", "locality", "country"]


class CompanyCountSerializer(serializers.Serializer):
    
    industry = serializers.CharField(required=False)
    size_range = serializers.CharField(required=False)
    locality = serializers.CharField(required=False)
    country = serializers.CharField(required=False)
    name = serializers.CharField(required=False)  # Add this field



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Replace with your UserProfile model
        fields = ['username', 'email', 'first_name', 'last_name', 'other_fields']  # Include other fields as needed
        
        

class UserListSerializer(ModelSerializer):
    class Meta:
        model = EmailAddress
        fields = ['id', 'user', 'email', 'verified', 'primary']
        