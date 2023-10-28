import asyncio
from asgiref.sync import async_to_sync, sync_to_async
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from app.models import Station
from rest_framework.decorators import api_view
import noise
from django.http import JsonResponse
from .serializers import StationSerializer
import numpy as np
#from app.tasks import print_hello



def say_hello(request):
    #print_hello.delay()  # Запускаем Celery задачу асинхронно
    return HttpResponse("Ok")

def generate_map(request):
    print("start generating...")
    width, height = 400, 400

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

# Преобразуем синхронные функции в асинхронные
async_set_current_position = sync_to_async(set_current_position)
async_get_station = sync_to_async(Station.objects.get)

# Асинхронный обработчик для обновления координат каждую секунду
async def update_coordinates(coordinates):
    while True:
        # Ваша логика обновления координат здесь
        x, y = coordinates[0]
        del coordinates[0]
        station = await async_get_station(station_id=1)

        # Используйте асинхронную транзакцию для безопасного обновления данных в базе данных
        async with transaction.atomic():
            station.current_x = x
            station.current_y = y
            await station.save()

        # Приостанавливаем выполнение на 1 секунду
        await asyncio.sleep(1)

# Глобальная переменная для хранения корутины
update_coordinates_task = None

# Обработчик для запуска асинхронного обновления координат
@api_view(['POST'])
async def start_update_coordinates(request):
    global update_coordinates_task

    if request.method == 'POST':
        data = request.POST
        print(f"\n\ndata = {data}\n\n")
        print(f"\n\ndata_x = {data.getlist('x')}\n\n")
        coordinates = data.getlist('x'), data.getlist('y')
        print(coordinates)

        # Остановим существующую корутину, если она существует
        if update_coordinates_task is not None:
            update_coordinates_task.cancel()

        # Создаем новую корутину для обновления координат
        update_coordinates_task = asyncio.ensure_future(update_coordinates(coordinates))

        return JsonResponse({'message': 'Update started.'})

    return JsonResponse({'message': 'Invalid request method.'})

# Обработчик для остановки асинхронного обновления координат
@csrf_exempt
def stop_update_coordinates(request):
    global update_coordinates_task

    if request.method == 'POST':
        # Останавливаем корутину, если она существует
        if update_coordinates_task is not None:
            update_coordinates_task.cancel()
            update_coordinates_task = None
            return JsonResponse({'message': 'Update stopped.'})

    return JsonResponse({'message': 'Invalid request method.'})

# Обработчик для получения текущих координат
def get_current_coordinates(request):
    station = Station.objects.get(station_id=1)
    serializer = StationSerializer(station)
    return JsonResponse(serializer.data)

