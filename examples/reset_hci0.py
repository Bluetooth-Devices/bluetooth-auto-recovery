import asyncio
import logging

from bluetooth_auto_recovery import recover_adapter

logging.basicConfig(level=logging.INFO)
logging.getLogger("bluetooth_auto_recovery").setLevel(logging.DEBUG)


async def run() -> None:
    await recover_adapter(0, "aa:bb:cc:dd:ee:ff")


asyncio.run(run())
