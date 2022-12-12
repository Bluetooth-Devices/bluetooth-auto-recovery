import asyncio
import logging

from bluetooth_auto_recovery import recover_adapter

logging.basicConfig(level=logging.INFO)
logging.getLogger("bluetooth_auto_recovery").setLevel(logging.DEBUG)


async def run() -> None:
    await recover_adapter(0, "00:1a:7d:da:71:13")


asyncio.run(run())
