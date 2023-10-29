import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

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
