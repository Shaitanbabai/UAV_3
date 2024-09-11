import airsim
import asyncio
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def get_telemetry(client):
    while True:
        state = client.getMultirotorState()
        position = state.kinematics_estimated.position
        velocity = state.kinematics_estimated.linear_velocity
        info_state = f"""
Позиция дрона: 
    x = {position.x_val:.2f}, y = {position.y_val:.2f}, z = {position.z_val:.2f}
Скорость дрона (м/с):
    x = {velocity.x_val:.2f}, y = {velocity.y_val:.2f}, z = {velocity.z_val:.2f}
"""
        logging.info(info_state)
        await asyncio.sleep(1)


async def mission_test(client: airsim.MultirotorClient):
    waypoints = [
        airsim.Vector3r(0, 0, -10),     # полет вверх
        airsim.Vector3r(10, 0, -10),    # полет прямо
        airsim.Vector3r(0, 10, -10),    # полет вправо
        airsim.Vector3r(-10, -10, -10)             # полет задом по диагонали влево
    ]
    velocity = 5
    for waypoint in waypoints:
        client.moveToPositionAsync(waypoint.x_val, waypoint.y_val, waypoint.z_val, velocity).join()
        await asyncio.sleep(2)

    await landing(client)

async def landing(client: airsim.MultirotorClient):
    z = client.getMultirotorState().kinematics_estimated.position.z_val
    logging.info(f"Текущая высота: {z} метров")

    if z < -5:
        logging.info("Высота выше 5 метров, начинаем снижение до 5 метров...")
        client.moveToPositionAsync(0, 0, -5, 5).join()
        await asyncio.sleep(2)

    logging.info("Начинаем посадку...")
    client.landAsync().join()



async def main():
    client = airsim.MultirotorClient()
    client.confirmConnection()

    client.enableApiControl(True)
    client.armDisarm(True)

    client.takeoffAsync().join()

    await asyncio.gather(
        get_telemetry(client),
        mission_test(client)
    )

    client.armDisarm(False)
    client.enableApiControl(False)


if __name__ == '__main__':
    asyncio.run(main())