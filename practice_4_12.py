# Как получать данные с AirSim в режиме реальной симуляции
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
Drone position:
    x: {position.x_val:2f}, y: {position.y_val:2f}, z: {position.z_val:2f}
Drone velocity: 
    vx: {velocity.x_val:2f}, vy: {velocity.y_val:2f}, vz: {velocity.z_val:2f}
"""
        logging.info(info_state)
        await asyncio.sleep(1)

async def mission_test(client):  # autonomous pre-set mission
    waypoints = [
        airsim.Vector3r(0, 0, -10),  # take altitude 10m
        airsim.Vector3r(10, 0, -10), # forward 10m
        airsim.Vector3r(0, 10, -10),  # to the right 10m
        airsim.Vector3r(-10, 10, -10),  # to the left  and back (diagonal)
        airsim.Vector3r(0, 0, 0) # halt
    ]
    velocity = 5
    for waypoint in waypoints:
        client.moveToPositionAsync(waypoint.x_val, waypoint.y_val, waypoint.z_val, velocity)
        await asyncio.sleep(2)

    await  manual_control(client)
    await landing(client)


async def manual_control(client: airsim.MultirotorClient):
    remote_control_data = airsim.RCData(pitch=0.5, # тангаж, наклон вперед 0 - 1 (0-100%)
                                        roll=0.0, # крен
                                        throttle=0.0, # тяга
                                        yaw=0.0, # вращение вокруг оси Z
                                        is_initialized=True,  # флаг инициализации
                                        is_valid=True,  # флаг валидности
                                        )
    client.moveByRCDataAsync(remote_control_data)
    await asyncio.sleep(5)
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


# creating client
# creating async function to switch to client
async def main(): # For tutorial simplicity classes not assigned. Commands shall be divided to classes
    client = airsim.MultirotorClient()
    client.confirmConnection()

    client.enableApiControl(True)  # processing switching, arming and flight
    client.armDisarm(True)

    client.takeoffAsync().join()  # calling async methodsset takeoff command

    # let to call and launch simultaneously several methods
    await asyncio.gather(get_telemetry(client),
                           mission_test(client),
                           manual_control(client))  # launching telemetry

    client.armDisarm(False)  # set disarm command
    client.enableApiControl(False)  # set disable api control

if __name__ == "__main__":
    asyncio.run(main())