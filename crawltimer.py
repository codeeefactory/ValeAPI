import time
import asyncio
async def countdown(seconds, callback):
    while seconds > 0:
        # print(f"Time remaining: {seconds} seconds")
        await asyncio.sleep(1)
        seconds -= 1
    await callback()  # Call the passed function after countdown
