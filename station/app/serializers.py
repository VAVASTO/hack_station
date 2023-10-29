from rest_framework import serializers
from .models import Station
from .models import Items
from .models import Wheels
from .models import SolarPanels
from .models import Other


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = ('current_x', 'current_y')


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ('item_id', 'station', 'name', 'item_index', 'status')

class MultipleItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items  # Укажите модель, которую вы хотите сериализовать
        fields = ('item_id', 'station', 'name', 'item_index', 'status')  # Укажите поля модели, которые вы хотите включить в сериализацию

class WheelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wheels
        fields = '__all__'

class SolarPanelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolarPanels
        fields = '__all__'

class OtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Other
        fields = '__all__'
