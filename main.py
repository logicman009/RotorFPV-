import asyncio

from config import TARGET_LAT
from config import TARGET_LON
from config import TARGET_ALTITUDE

from drone_control import DroneController
from vision import VisionSystem
from payload import PayloadSystem
from navigation import NavigationSystem


async def main():
    drone = DroneController()

    vision = VisionSystem()

    payload = PayloadSystem()

    navigation = NavigationSystem(
        drone,
        vision,
        payload
    )

    await drone.connect()

    telemetry_task = asyncio.create_task(
        drone.print_telemetry()
    )

    await drone.wait_for_global_position()

    await drone.arm()

    await drone.takeoff()

    await drone.goto_location(
        TARGET_LAT,
        TARGET_LON,
        TARGET_ALTITUDE
    )

    print("Waiting to reach target area")

    await asyncio.sleep(15)

    await drone.start_offboard()

    qr_data = await navigation.visual_align_and_drop()

    print(f"Decoded QR Data: {qr_data}")

    print("Mission complete")

    await drone.land()

    telemetry_task.cancel()

    vision.release()


if __name__ == "__main__":
    asyncio.run(main())
