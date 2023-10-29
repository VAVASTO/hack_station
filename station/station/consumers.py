import asyncio
import json
import numpy as np
import noise
from app.models import Station
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from app.serializers import StationSerializer

running = False

class SomeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        global running
        running = True
        asyncio.create_task(self.background_task())

    async def disconnect(self, close_code):
        # Установить флаг running в False, чтобы завершить задачу
        pass        

    async def receive(self, text_data):
        # Обработка полученных данных
        if text_data == "stop_task":
            # Получена команда для остановки задачи
            global running
            running = False

    async def background_task(self):
        while running:
            print("hello_world")
            await asyncio.sleep(1)


class GetMap(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass     

    async def receive(self, text_data):
        print("start generating...")
        print(text_data)
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

        #await self.send(text_data=json.dumps(world.tolist()))      
        while True:
            await self.send(text_data=json.dumps(world.tolist()))
            await asyncio.sleep(1)
            
        

class TurnAutopilotOn(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass        

    async def receive(self, text_data):
        print(text_data)
        json_data = json.loads(text_data)
        formatted_data_string = json_data.replace("'", "\"")

        json_data = json.loads(formatted_data_string)
        get_station = sync_to_async(Station.objects.get)
        while True:

            station = await get_station(station_id=1)
            if len(json_data["x"]) != 0:
                get_station = sync_to_async(Station.objects.get)
                save_station = sync_to_async(lambda station: station.save())

                
                x, y = json_data["x"][0], json_data["y"][0] 
                print(x, y)
                station.current_x = x
                station.current_y = y
                print(station.current_x, station.current_y)

                await save_station(station) 

                serializer = StationSerializer(station)
                del json_data["x"][0], json_data["y"][0]
                
                data_to_send = {
                "current_position": serializer.data,
                "path": json_data
                }


                await self.send(json.dumps(data_to_send))
                await asyncio.sleep(0.1)
            

            serializer = StationSerializer(station)
            data_to_send = {
            "current_position": serializer.data,
            "path": json_data
            }

class GetPosition(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass     

    async def receive(self, text_data):
        get_station = sync_to_async(Station.objects.get)
        
        station = await get_station(station_id=1)
        serializer = StationSerializer(station)
        await self.send(text_data=json.dumps(serializer.data))

class SetPosition(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass     

    
    async def receive(self, text_data):
        get_station = sync_to_async(Station.objects.get)
        save_station = sync_to_async(lambda station: station.save())

        station = await get_station(station_id=1)
        print(text_data)
        splited_data = text_data.split()
        x, y = splited_data[0], splited_data[1]
        print(x, y)
        station.current_x = x
        station.current_y = y
        print(station.current_x, station.current_y)

        await save_station(station)  # Use sync_to_async for the save operation

        serializer = StationSerializer(station)
        await self.send(text_data=json.dumps(serializer.data))
