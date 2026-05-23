from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator
from unittest.mock import AsyncMock, MagicMock

import pytest

from bluetooth_auto_recovery.recover import MGMTBluetoothCtl


@pytest.fixture
def adapter() -> MGMTBluetoothCtl:
    """A fully-resolved adapter with an AsyncMock protocol."""
    ctl = MGMTBluetoothCtl("hci0", "AA:BB:CC:DD:EE:FF", 5)
    ctl.idx = 0
    ctl.hci_name = "hci0"
    ctl.mac = "AA:BB:CC:DD:EE:FF"
    ctl.protocol = AsyncMock()
    return ctl


def make_send_response(*, status: int = 0x00) -> MagicMock:
    """Build a fake btmgmt protocol response."""
    response = MagicMock()
    response.event_frame.status.value = status
    return response


@asynccontextmanager
async def adapter_cm(
    value: MGMTBluetoothCtl | None,
) -> AsyncIterator[MGMTBluetoothCtl | None]:
    """Yield a value as an async context manager (stand-in for _get_adapter)."""
    yield value
