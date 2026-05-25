from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import bluetooth_auto_recovery
from bluetooth_auto_recovery import recover

# Capture the package-level wrapper before any test rebinds the name on the
# package module (test_recover_adapter rebinds it).
_RECOVER_ADAPTER_WRAPPER = bluetooth_auto_recovery.recover_adapter


def test_init():
    """Test the init function."""
    assert bluetooth_auto_recovery


@pytest.mark.asyncio
async def test_recover_adapter():
    """Test the recover_adapter function."""
    assert bluetooth_auto_recovery.recover_adapter is not recover.recover_adapter

    with patch("bluetooth_auto_recovery.recover.recover_adapter") as recover_adapter:
        await bluetooth_auto_recovery.recover_adapter(0, "00:00:00:00:00:00")

    assert recover_adapter.called
    assert bluetooth_auto_recovery.recover_adapter is recover_adapter
    bluetooth_auto_recovery.recover_adapter = recover.recover_adapter


@pytest.mark.asyncio
async def test_recover_adapter_uses_cached_module():
    """A cached recover module is reused without re-importing."""
    key = f"{bluetooth_auto_recovery.__name__}.recover"
    mock_module = MagicMock()
    mock_module.recover_adapter = AsyncMock(return_value=True)

    prev = bluetooth_auto_recovery._MODULE_CACHE.get(key)
    bluetooth_auto_recovery._MODULE_CACHE[key] = mock_module
    try:
        result = await _RECOVER_ADAPTER_WRAPPER(1, "AA:BB:CC:DD:EE:FF", True)
    finally:
        if prev is None:
            bluetooth_auto_recovery._MODULE_CACHE.pop(key, None)
        else:
            bluetooth_auto_recovery._MODULE_CACHE[key] = prev

    assert result is True
    mock_module.recover_adapter.assert_awaited_once_with(1, "AA:BB:CC:DD:EE:FF", True)
