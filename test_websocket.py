import asyncio
import websockets

async def test_websocket_connection():
    uri = "ws://localhost:8000/ws/route/generate/"  # Замените на ваш адрес веб-сокета

    async with websockets.connect(uri) as websocket:
        # Отправляем сообщение на веб-сокет сервер
        message_to_send = "stop_task"
        await websocket.send(message_to_send)
        print(f"Sent: {message_to_send}")

        # Принимаем сообщение от веб-сокет сервера
        response = await websocket.recv()
        print(f"Received: {response}")

# Запускаем тестовое соединение
asyncio.get_event_loop().run_until_complete(test_websocket_connection())
