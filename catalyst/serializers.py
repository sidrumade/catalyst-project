from rest_framework import serializers
from .models import Company

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
