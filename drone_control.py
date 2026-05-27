from mavsdk import System
from mavsdk.offboard import VelocityNedYaw
import asyncio


class DroneController:
    def __init__(self):
        self.drone = System()

    async def connect(self):
        await self.drone.connect(system_address="udp://:14540")

        print("Waiting for drone connection...")

        async for state in self.drone.core.connection_state():
            if state.is_connected:
                print("Drone connected")
                break

    async def wait_for_global_position(self):
        print("Waiting for GPS lock...")

        async for health in self.drone.telemetry.health():
            if health.is_global_position_ok and health.is_home_position_ok:
                print("GPS lock acquired")
                break

    async def arm(self):
        print("Arming drone")
        await self.drone.action.arm()

    async def takeoff(self):
        print("Taking off")
        await self.drone.action.takeoff()
        await asyncio.sleep(8)

    async def goto_location(self, lat, lon, alt, yaw=0):
        print(f"Flying to GPS target: {lat}, {lon}")
        await self.drone.action.goto_location(lat, lon, alt, yaw)

    async def start_offboard(self):
        print("Starting Offboard Mode")

        await self.drone.offboard.set_velocity_ned(
            VelocityNedYaw(0.0, 0.0, 0.0, 0.0)
        )

        await self.drone.offboard.start()

    async def send_velocity(self, vx, vy, vz=0.0, yaw=0.0):
        await self.drone.offboard.set_velocity_ned(
            VelocityNedYaw(vx, vy, vz, yaw)
        )

    async def stop(self):
        await self.send_velocity(0.0, 0.0, 0.0)

    async def land(self):
        print("Landing")
        await self.drone.action.land()

    async def print_telemetry(self):
        async for position in self.drone.telemetry.position():
            print(
                f"LAT: {position.latitude_deg:.6f} | "
                f"LON: {position.longitude_deg:.6f} | "
                f"ALT: {position.relative_altitude_m:.2f}"
            )
            await asyncio.sleep(1)
