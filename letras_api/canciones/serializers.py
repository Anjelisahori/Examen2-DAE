from rest_framework import serializers
from .models import LetraCancion

class LetraCancionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LetraCancion
        fields = '__all__'
