import websockets
import asyncio
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, filemode="w")

class SecureProxy:
    def __init__(self, control_drone):
        # Инициализация прокси с функцией управления дроном
        self.control_drone = control_drone

    async def __call__(self, websocket, path):
        # Обработка входящих сообщений по вебсокету
        async for msg in websocket:
            # Проверка авторизации
            if self.is_auth(websocket):
                # Если авторизация прошла, передаем управление дроном
                await self.control_drone(websocket, path, msg)
            else:
                # Если авторизация не прошла, отправляем сообщение об ошибке
                await websocket.send("Неавторизированный доступ")

    def is_auth(self, websocket):
        try:
            # Проверка наличия параметров в пути вебсокета
            if "?" in websocket.path:
                params = websocket.path.split("?")[1]
                # Обработка параметров, разделенных амперсандом, и проверка наличия "="
                params = dict(param.split("=") for param in params.split("&") if "=" in param)
                # Проверка токена на валидность
                return params.get("token") == "valid_token"
        except Exception as e:
            # Логирование ошибки аутентификации
            logging.info(f"Ошибка аутентификации: {e}")
        return False

async def control_drone(websocket, path, msg):
    # path передаётся как параметр, но в текущем коде он не используется.
    # Его можно было бы использовать для различения команд,
    # приходящих по разным путям URL, если бы было необходимо.
    # if path == "/control/takeoff":
    #   if msg == "takeoff":
    #       await websocket.send("Дрон взлетает")
    try:
        # Логирование полученной команды
        logging.info(f"Получена команда: {msg}")
        # print(f"Получена команда: {msg}") # Закомментировано для логирования
        if msg == "takeoff":
            # Логирование и отправка команды взлета
            logging.info(f"Дрон взлетает")
            await websocket.send("Дрон взлетает")
        elif msg == "land":
            # Логирование и отправка команды приземления
            logging.info(f"Дрон приземляется")
            await websocket.send("Дрон приземляется")
    except websockets.ConnectionClosed as e:
        # Логирование закрытия соединения
        logging.info(f"Соединение закрыто: {e}")
    except Exception as e:
        # Логирование прочих исключений
        logging.info(e)

async def main():
    # Создание экземпляра прокси
    proxy = SecureProxy(control_drone)
    # Запуск вебсокет-сервера
    async with websockets.serve(proxy, host="localhost", port=8765) as server:
        try:
            # Ожидание закрытия сервера
            await server.wait_closed()
        except Exception as e:
            # Логирование ошибок при работе сервера
            logging.info(e)
            logging.info("Сервер закрыт")

if __name__ == '__main__':
    # Запуск главной асинхронной функции
    asyncio.run(main())
