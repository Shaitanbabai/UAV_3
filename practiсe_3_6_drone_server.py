import websockets
import asyncio


async def control_drone(websocket, path):
    try:
        async for msg in websocket:
            print(f"Получена команда: {msg}")
            if msg == "takeoff":
                print(f"Дрон взлетает")
                await websocket.send("Дрон взлетает")
            elif msg == "land":
                print(f"Дрон приземляется")
                await websocket.send("Дрон приземляется")
    except websockets.ConnectionClosed as e:
        print(f"Соединение закрыто: {e}")
    except Exception as e:
        print(e)

start_server = websockets.serve(control_drone, host="localhost", port=8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()