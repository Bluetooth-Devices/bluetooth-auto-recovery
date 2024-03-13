from unittest.mock import patch

import pytest

import bluetooth_auto_recovery


def test_init():
    """Test the init function."""
    assert bluetooth_auto_recovery


@pytest.mark.asyncio
async def test_recover_adapter():
    """Test the recover_adapter function."""
    with patch("bluetooth_auto_recovery.recover_adapter") as recover_adapter:
        await bluetooth_auto_recovery.recover_adapter(0, "00:00:00:00:00:00")

    assert recover_adapter.called
