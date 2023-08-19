from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["industry", "size_range", "locality", "country"]


class CompanyCountSerializer(serializers.Serializer):
    industry = serializers.CharField()
    size_range = serializers.CharField()
    locality = serializers.CharField()
    country = serializers.CharField()