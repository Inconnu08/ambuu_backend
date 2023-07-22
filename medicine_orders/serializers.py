from rest_framework import serializers
from .models import MedicineOrder


class MedicineOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineOrder
        fields = '__all__'
