import asyncio
from config import KP
from config import ALIGNMENT_THRESHOLD
from config import HOVER_TIME_BEFORE_DROP


class NavigationSystem:
    def __init__(self, drone, vision, payload):
        self.drone = drone
        self.vision = vision
        self.payload = payload

    async def visual_align_and_drop(self):
        print("Searching for QR code...")

        stable_counter = 0

        while True:
            frame = self.vision.get_frame()

            if frame is None:
                continue

            result = self.vision.detect_qr(frame)

            if result is None:
                print("QR not detected")

                await self.drone.send_velocity(0.0, 0.0, 0.0)

                await asyncio.sleep(0.1)
                continue

            print(f"QR Data: {result['data']}")
            print(f"Error X: {result['error_x']}")
            print(f"Error Y: {result['error_y']}")

            error_x = result['error_x']
            error_y = result['error_y']

            vx = -KP * error_y
            vy = -KP * error_x

            print(f"Velocity Command -> VX: {vx:.3f}, VY: {vy:.3f}")

            await self.drone.send_velocity(vx, vy)

            aligned_x = abs(error_x) < ALIGNMENT_THRESHOLD
            aligned_y = abs(error_y) < ALIGNMENT_THRESHOLD

            if aligned_x and aligned_y:
                stable_counter += 1
                print(f"Alignment stable: {stable_counter}")
            else:
                stable_counter = 0

            if stable_counter >= HOVER_TIME_BEFORE_DROP * 10:
                print("Target aligned")

                await self.drone.stop()

                self.payload.drop_payload()

                return result['data']

            await asyncio.sleep(0.1)
