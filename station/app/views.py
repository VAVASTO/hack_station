import asyncio
from asgiref.sync import async_to_sync, sync_to_async
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from app.models import Station
from app.models import Items
from app.models import Wheels
from app.models import SolarPanels
from app.models import Other
from rest_framework.decorators import api_view
import noise
from django.http import JsonResponse
from .serializers import StationSerializer
from .serializers import ItemsSerializer
from .serializers import MultipleItemsSerializer
from .serializers import WheelsSerializer
from .serializers import SolarPanelsSerializer
from .serializers import OtherSerializer
import numpy as np
#from app.tasks import print_hello



def say_hello(request):
    #print_hello.delay()  # Запускаем Celery задачу асинхронно
    return HttpResponse("Ok")

def generate_map(request):
    print("start generating...")
    width, height = 100, 100

    scale = 100
    octaves = 6
    persistence = 0.5

    world = np.zeros((width, height))
    for i in range(width):
        for j in range(height):
            world[i][j] = noise.pnoise2(i / scale,
                                    j / scale,
                                    octaves=octaves,
                                    persistence=persistence,
                                    repeatx=1024,
                                    repeaty=1024,
                                    base=42)

    world = (world - np.min(world)) / (np.max(world) - np.min(world)) * 100
    world = world.astype(int)

    print("map generated!")

    return HttpResponse(world)

@api_view(["POST"])
def set_current_position(request):
    station = Station.objects.get(station_id=1)
    x, y = request.data['x'], request.data['y']
    print(x, y)
    station.current_x = x
    station.current_y = y
    print(station.current_x, station.current_y)
    station.save()
    return HttpResponse("yep")

def get_current_coordinates(request):
    station = Station.objects.get(station_id=1)
    serializer = StationSerializer(station)
    return JsonResponse(serializer.data)

@api_view(['POST'])
def break_something(request):
    name = request.data.get('name')
    item_index = request.data.get('item_id')
    new_status = request.data.get('status')
    print(name, item_index, new_status)
    try:
        item = Items.objects.get(name=name, item_index=item_index)
        item.status = new_status
        item.save()  
        return HttpResponse("Item status updated successfully.")
    except Items.DoesNotExist:
        return HttpResponse("Item not found.", status=404)
    
@api_view(['GET'])
def get_broken_detail(request):
    try:
        item = Items.objects.get(status="Требует замены")
        serializer = ItemsSerializer(item)  # Serialize the item object
        return JsonResponse(serializer.data)
    except Items.DoesNotExist:
        return HttpResponse("Item not found", status=404)
    
@api_view(['GET'])
def get_details(request):
    try:
        items = Items.objects.all()  # Получите все объекты модели Items
        serializer = MultipleItemsSerializer(items, many=True)  # Сериализуйте список объектов
        return JsonResponse(serializer.data, safe=False)
    except Items.DoesNotExist:
        return HttpResponse("Items not found", status=404)
    

@api_view(['GET'])
def get_wheels(request):
    try:
        items = Wheels.objects.all()  # Получите все объекты модели Items
        serializer = WheelsSerializer(items, many=True)  # Сериализуйте список объектов
        return JsonResponse(serializer.data, safe=False)
    except Wheels.DoesNotExist:
        return HttpResponse("Items not found", status=404)
    

@api_view(['GET'])
def get_solar_panel(request):
    try:
        items = SolarPanels.objects.all()  # Получите все объекты модели Items
        serializer = SolarPanelsSerializer(items, many=True)  # Сериализуйте список объектов
        return JsonResponse(serializer.data, safe=False)
    except SolarPanels.DoesNotExist:
        return HttpResponse("Items not found", status=404)
    
@api_view(['GET'])
def get_other(request):
    try:
        items = Other.objects.all()  # Получите все объекты модели Items
        serializer = OtherSerializer(items, many=True)  # Сериализуйте список объектов
        return JsonResponse(serializer.data, safe=False)
    except Other.DoesNotExist:
        return HttpResponse("Items not found", status=404)
