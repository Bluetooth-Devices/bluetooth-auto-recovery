"""Tests for the recover.py state machine."""

from __future__ import annotations

import asyncio
import errno
import logging
from typing import cast
from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest

from bluetooth_auto_recovery import recover
from bluetooth_auto_recovery.recover import (
    BluetoothMGMTProtocol,
    MGMTBluetoothCtl,
    RFKillInfo,
    hci_name_to_number,
    raw_close,
    raw_open,
    rfkill_list_bluetooth,
    rfkill_unblock,
)

from .conftest import adapter_cm, make_send_response

# ---------------------------------------------------------------------------
# Pure helpers
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("name", "expected"),
    [("hci0", 0), ("hci1", 1), ("hci15", 15), ("hci255", 255)],
)
def test_hci_name_to_number(name: str, expected: int) -> None:
    assert hci_name_to_number(name) == expected


def test_rfkill_info_dataclass() -> None:
    info = RFKillInfo(soft_block=True, hard_block=False, idx=3)
    assert info.soft_block is True
    assert info.hard_block is False
    assert info.idx == 3


# ---------------------------------------------------------------------------
# rfkill_list_bluetooth
# ---------------------------------------------------------------------------


def test_rfkill_list_bluetooth_success(adapter: MGMTBluetoothCtl) -> None:
    rfkill_mod = MagicMock()
    rfkill_mod.rfkill_list.return_value = {
        "hci0": {"soft": True, "hard": False, "idx": 7}
    }
    with patch.object(recover, "rfkill", rfkill_mod):
        info = rfkill_list_bluetooth(adapter)
    assert info == RFKillInfo(soft_block=True, hard_block=False, idx=7)


@pytest.mark.parametrize(
    "exc",
    [
        FileNotFoundError(),
        IndexError(),
        PermissionError(),
        UnicodeDecodeError("utf-8", b"", 0, 1, "bad"),
        RuntimeError("boom"),
    ],
)
def test_rfkill_list_bluetooth_handles_errors(
    adapter: MGMTBluetoothCtl, exc: Exception
) -> None:
    rfkill_mod = MagicMock()
    rfkill_mod.rfkill_list.side_effect = exc
    with patch.object(recover, "rfkill", rfkill_mod):
        info = rfkill_list_bluetooth(adapter)
    assert info == RFKillInfo(None, None, None)


def test_rfkill_list_bluetooth_adapter_not_in_results(
    adapter: MGMTBluetoothCtl,
) -> None:
    rfkill_mod = MagicMock()
    rfkill_mod.rfkill_list.return_value = {
        "hci9": {"soft": False, "hard": False, "idx": 1}
    }
    with patch.object(recover, "rfkill", rfkill_mod):
        info = rfkill_list_bluetooth(adapter)
    assert info == RFKillInfo(None, None, None)


# ---------------------------------------------------------------------------
# rfkill_unblock
# ---------------------------------------------------------------------------


def test_rfkill_unblock_success(adapter: MGMTBluetoothCtl) -> None:
    rfkill_mod = MagicMock()
    rfkill_mod.dpath = "/dev/rfkill"
    rfkh_mod = MagicMock()
    rfkh_mod.rfkill_event.return_value = b"event"
    with (
        patch.object(recover, "rfkill", rfkill_mod),
        patch.object(recover, "rfkh", rfkh_mod),
        patch("builtins.open", MagicMock()),
    ):
        assert rfkill_unblock(adapter, 7) is True


def test_rfkill_unblock_failure(adapter: MGMTBluetoothCtl) -> None:
    rfkill_mod = MagicMock()
    rfkill_mod.dpath = "/dev/rfkill"
    with (
        patch.object(recover, "rfkill", rfkill_mod),
        patch("builtins.open", side_effect=OSError("nope")),
    ):
        assert rfkill_unblock(adapter, 7) is False


# ---------------------------------------------------------------------------
# MGMTBluetoothCtl basics
# ---------------------------------------------------------------------------


def test_name_property(adapter: MGMTBluetoothCtl) -> None:
    assert adapter.name == "hci0 [AA:BB:CC:DD:EE:FF] (0)"


@pytest.mark.asyncio
async def test_close_closes_transport_and_socket() -> None:
    ctl = MGMTBluetoothCtl("hci0", "AA:BB:CC:DD:EE:FF", 5)
    transport = MagicMock()
    protocol = MagicMock()
    protocol.transport = transport
    ctl.protocol = cast("BluetoothMGMTProtocol | None", protocol)
    ctl.sock = MagicMock()
    with patch.object(recover.btmgmt_socket, "close") as mock_close:
        await ctl.close()
    transport.close.assert_called_once()
    assert ctl.protocol is None
    mock_close.assert_called_once_with(ctl.sock)


@pytest.mark.asyncio
async def test_close_no_protocol() -> None:
    ctl = MGMTBluetoothCtl("hci0", "AA:BB:CC:DD:EE:FF", 5)
    ctl.protocol = None
    ctl.sock = MagicMock()
    with patch.object(recover.btmgmt_socket, "close") as mock_close:
        await ctl.close()
    mock_close.assert_called_once_with(ctl.sock)


@pytest.mark.asyncio
async def test_get_powered(adapter: MGMTBluetoothCtl) -> None:
    response = MagicMock()
    response.cmd_response_frame.current_settings.get.return_value = True
    cast(AsyncMock, adapter.protocol).send.return_value = response
    assert await adapter.get_powered() is True


@pytest.mark.asyncio
async def test_get_powered_no_idx(adapter: MGMTBluetoothCtl) -> None:
    adapter.idx = None
    assert await adapter.get_powered() is None


@pytest.mark.asyncio
async def test_set_powered_success(adapter: MGMTBluetoothCtl) -> None:
    cast(AsyncMock, adapter.protocol).send.return_value = make_send_response(
        status=0x00
    )
    assert await adapter.set_powered(True) is True


@pytest.mark.asyncio
async def test_set_powered_failure(adapter: MGMTBluetoothCtl) -> None:
    cast(AsyncMock, adapter.protocol).send.return_value = make_send_response(
        status=0x01
    )
    assert await adapter.set_powered(True) is False


@pytest.mark.asyncio
async def test_wait_for_power_state_reaches_target(adapter: MGMTBluetoothCtl) -> None:
    with patch.object(adapter, "get_powered", AsyncMock(return_value=True)):
        assert await adapter.wait_for_power_state(True, 1) is True


@pytest.mark.asyncio
async def test_wait_for_power_state_times_out(adapter: MGMTBluetoothCtl) -> None:
    with patch.object(adapter, "get_powered", AsyncMock(return_value=False)):
        # Never reaches True -> returns last observed state on timeout.
        assert await adapter.wait_for_power_state(True, 0.05) is False


# ---------------------------------------------------------------------------
# MGMTBluetoothCtl._find_controller
# ---------------------------------------------------------------------------


def _ctl() -> MGMTBluetoothCtl:
    ctl = MGMTBluetoothCtl("hci0", "AA:BB:CC:DD:EE:FF", 5)
    ctl.protocol = AsyncMock()
    return ctl


@pytest.mark.asyncio
async def test_find_controller_match_by_mac_from_hci() -> None:
    ctl = _ctl()
    adapters = {
        "hci0": {"dev_id": 0, "name": "hci0", "bdaddr": "AA:BB:CC:DD:EE:FF"},
    }
    with patch.object(recover, "get_adapters_from_hci", return_value=adapters):
        await ctl._find_controller()
    assert ctl.idx == 0
    assert ctl.hci_name == "hci0"
    assert ctl.mac == "AA:BB:CC:DD:EE:FF"
    cast(AsyncMock, ctl.protocol).send.assert_not_called()


@pytest.mark.asyncio
async def test_find_controller_match_by_name_from_hci() -> None:
    ctl = _ctl()
    adapters = {
        "hci0": {"dev_id": 3, "name": "hci0", "bdaddr": "11:22:33:44:55:66"},
    }
    with patch.object(recover, "get_adapters_from_hci", return_value=adapters):
        await ctl._find_controller()
    # MAC did not match, but the hci name did.
    assert ctl.idx == 3
    assert ctl.hci_name == "hci0"
    assert ctl.mac == "11:22:33:44:55:66"


@pytest.mark.asyncio
async def test_find_controller_match_by_mac_via_controller_info() -> None:
    ctl = _ctl()
    idx_response = MagicMock()
    idx_response.event_frame.status.value = 0x00
    idx_response.cmd_response_frame.num_controllers = 1
    setattr(idx_response.cmd_response_frame, "controller_index[i]", [5])

    info_response = MagicMock()
    info_response.cmd_response_frame.address = "aa:bb:cc:dd:ee:ff"

    cast(AsyncMock, ctl.protocol).send = AsyncMock(
        side_effect=[idx_response, info_response]
    )
    with patch.object(recover, "get_adapters_from_hci", return_value={}):
        await ctl._find_controller()
    assert ctl.idx == 5
    assert ctl.hci_name == "hci5"
    assert ctl.mac == "AA:BB:CC:DD:EE:FF"


@pytest.mark.asyncio
async def test_find_controller_fallback_by_hci_number() -> None:
    ctl = _ctl()
    idx_response = MagicMock()
    idx_response.event_frame.status.value = 0x00
    idx_response.cmd_response_frame.num_controllers = 1
    setattr(idx_response.cmd_response_frame, "controller_index[i]", [0])

    info_response = MagicMock()
    # MAC differs from expected, so it falls back to matching by hci number 0.
    info_response.cmd_response_frame.address = "99:99:99:99:99:99"

    cast(AsyncMock, ctl.protocol).send = AsyncMock(
        side_effect=[idx_response, info_response]
    )
    with patch.object(recover, "get_adapters_from_hci", return_value={}):
        await ctl._find_controller()
    assert ctl.idx == 0
    assert ctl.hci_name == "hci0"
    assert ctl.mac == "99:99:99:99:99:99"


@pytest.mark.asyncio
async def test_find_controller_index_list_error_status() -> None:
    ctl = _ctl()
    idx_response = MagicMock()
    idx_response.event_frame.status.value = 0x01  # non-success
    cast(AsyncMock, ctl.protocol).send = AsyncMock(return_value=idx_response)
    with patch.object(recover, "get_adapters_from_hci", return_value={}):
        await ctl._find_controller()
    assert ctl.idx is None


@pytest.mark.asyncio
async def test_find_controller_no_controllers() -> None:
    ctl = _ctl()
    idx_response = MagicMock()
    idx_response.event_frame.status.value = 0x00
    idx_response.cmd_response_frame.num_controllers = 0
    cast(AsyncMock, ctl.protocol).send = AsyncMock(return_value=idx_response)
    with patch.object(recover, "get_adapters_from_hci", return_value={}):
        await ctl._find_controller()
    assert ctl.idx is None


# ---------------------------------------------------------------------------
# _check_rfkill / _unblock_rfkill
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_check_rfkill_success(adapter: MGMTBluetoothCtl) -> None:
    info = RFKillInfo(soft_block=False, hard_block=False, idx=2)
    with patch.object(recover, "rfkill_list_bluetooth", return_value=info):
        assert await recover._check_rfkill(adapter) == info


@pytest.mark.asyncio
async def test_check_rfkill_timeout(adapter: MGMTBluetoothCtl) -> None:
    with patch.object(
        recover, "rfkill_list_bluetooth", side_effect=lambda a: _block_forever()
    ):
        # asyncio_timeout wraps the executor call; force it to expire fast.
        with patch.object(recover, "MAX_RFKILL_TIME", 0.01):
            result = await recover._check_rfkill(adapter)
    assert result == RFKillInfo(None, None, None)


def _block_forever() -> RFKillInfo:
    import time

    time.sleep(0.2)
    return RFKillInfo(None, None, None)


@pytest.mark.asyncio
async def test_unblock_rfkill_success(adapter: MGMTBluetoothCtl) -> None:
    with patch.object(recover, "rfkill_unblock", return_value=True):
        assert await recover._unblock_rfkill(adapter, 3) is True


@pytest.mark.asyncio
async def test_unblock_rfkill_timeout(adapter: MGMTBluetoothCtl) -> None:
    with patch.object(
        recover, "rfkill_unblock", side_effect=lambda a, idx: _block_forever()
    ):
        # asyncio_timeout wraps the executor call; force it to expire fast.
        with patch.object(recover, "MAX_RFKILL_TIME", 0.01):
            assert await recover._unblock_rfkill(adapter, 3) is False


# ---------------------------------------------------------------------------
# _check_or_unblock_rfkill
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_check_or_unblock_idx_none(adapter: MGMTBluetoothCtl) -> None:
    with patch.object(
        recover, "_check_rfkill", AsyncMock(return_value=RFKillInfo(None, None, None))
    ):
        assert await recover._check_or_unblock_rfkill(adapter) is True


@pytest.mark.asyncio
async def test_check_or_unblock_hard_block(adapter: MGMTBluetoothCtl) -> None:
    info = RFKillInfo(soft_block=False, hard_block=True, idx=1)
    with patch.object(recover, "_check_rfkill", AsyncMock(return_value=info)):
        assert await recover._check_or_unblock_rfkill(adapter) is False


@pytest.mark.asyncio
async def test_check_or_unblock_not_soft_blocked(adapter: MGMTBluetoothCtl) -> None:
    info = RFKillInfo(soft_block=False, hard_block=False, idx=1)
    with patch.object(recover, "_check_rfkill", AsyncMock(return_value=info)):
        assert await recover._check_or_unblock_rfkill(adapter) is True


@pytest.mark.asyncio
async def test_check_or_unblock_soft_block_then_clear(
    adapter: MGMTBluetoothCtl,
) -> None:
    blocked = RFKillInfo(soft_block=True, hard_block=False, idx=1)
    cleared = RFKillInfo(soft_block=False, hard_block=False, idx=1)
    with (
        patch.object(
            recover, "_check_rfkill", AsyncMock(side_effect=[blocked, cleared])
        ),
        patch.object(recover, "_unblock_rfkill", AsyncMock(return_value=True)),
        patch.object(recover.asyncio, "sleep", AsyncMock()),
    ):
        assert await recover._check_or_unblock_rfkill(adapter) is True


@pytest.mark.asyncio
async def test_check_or_unblock_soft_block_still_blocked(
    adapter: MGMTBluetoothCtl,
) -> None:
    blocked = RFKillInfo(soft_block=True, hard_block=False, idx=1)
    with (
        patch.object(
            recover, "_check_rfkill", AsyncMock(side_effect=[blocked, blocked])
        ),
        patch.object(recover, "_unblock_rfkill", AsyncMock(return_value=True)),
        patch.object(recover.asyncio, "sleep", AsyncMock()),
    ):
        assert await recover._check_or_unblock_rfkill(adapter) is False


# ---------------------------------------------------------------------------
# _power_cycle_adapter
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_power_cycle_success(adapter: MGMTBluetoothCtl) -> None:
    with patch.object(recover, "_execute_reset", AsyncMock(return_value=True)):
        assert await recover._power_cycle_adapter(adapter) is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exc",
    [
        recover.btmgmt_socket.BluetoothSocketError("no socket"),
        OSError("io"),
        asyncio.TimeoutError(),
    ],
)
async def test_power_cycle_handles_errors(
    adapter: MGMTBluetoothCtl, exc: Exception
) -> None:
    with patch.object(recover, "_execute_reset", AsyncMock(side_effect=exc)):
        assert await recover._power_cycle_adapter(adapter) is False


@pytest.mark.asyncio
async def test_power_cycle_timeout_logs_timeout_message(
    adapter: MGMTBluetoothCtl, caplog: pytest.LogCaptureFixture
) -> None:
    with (
        patch.object(
            recover, "_execute_reset", AsyncMock(side_effect=asyncio.TimeoutError())
        ),
        caplog.at_level(logging.WARNING),
    ):
        assert await recover._power_cycle_adapter(adapter) is False
    assert "due to timeout" in caplog.text


# ---------------------------------------------------------------------------
# _usb_reset_adapter
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_usb_reset_success(adapter: MGMTBluetoothCtl) -> None:
    dev = MagicMock()
    dev.async_reset = AsyncMock(return_value=True)
    with patch.object(recover, "BluetoothDevice", return_value=dev):
        assert await recover._usb_reset_adapter(adapter) is True


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exc",
    [
        PermissionError(2, "denied", "/dev/foo"),
        RuntimeError("unexpected"),
    ],
)
async def test_usb_reset_handles_errors(
    adapter: MGMTBluetoothCtl, exc: Exception
) -> None:
    dev = MagicMock()
    dev.async_reset = AsyncMock(side_effect=exc)
    with patch.object(recover, "BluetoothDevice", return_value=dev):
        assert await recover._usb_reset_adapter(adapter) is False


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exc",
    [
        recover.NotAUSBDeviceError(),
        FileNotFoundError(),
    ],
)
async def test_usb_reset_not_applicable_returns_none(
    adapter: MGMTBluetoothCtl, exc: Exception
) -> None:
    # A non-USB adapter (no USB device behind the hci) is "not applicable",
    # signalled by None — distinct from an attempted-but-failed USB reset.
    dev = MagicMock()
    dev.async_reset = AsyncMock(side_effect=exc)
    with patch.object(recover, "BluetoothDevice", return_value=dev):
        assert await recover._usb_reset_adapter(adapter) is None


# ---------------------------------------------------------------------------
# _execute_power_on
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_execute_power_on_success(adapter: MGMTBluetoothCtl) -> None:
    with (
        patch.object(adapter, "set_powered", AsyncMock(return_value=True)),
        patch.object(adapter, "wait_for_power_state", AsyncMock(return_value=True)),
    ):
        assert (
            await recover._execute_power_on(adapter, power_state_before_reset=False)
            is True
        )


@pytest.mark.asyncio
async def test_execute_power_on_was_already_on(adapter: MGMTBluetoothCtl) -> None:
    # power_state_before_reset is True: takes the "is ON after power cycle" branch.
    with (
        patch.object(adapter, "set_powered", AsyncMock(return_value=True)),
        patch.object(adapter, "wait_for_power_state", AsyncMock(return_value=True)),
    ):
        assert (
            await recover._execute_power_on(adapter, power_state_before_reset=True)
            is True
        )


@pytest.mark.asyncio
async def test_execute_power_on_state_false(adapter: MGMTBluetoothCtl) -> None:
    with (
        patch.object(adapter, "set_powered", AsyncMock(return_value=True)),
        patch.object(adapter, "wait_for_power_state", AsyncMock(return_value=False)),
    ):
        assert (
            await recover._execute_power_on(adapter, power_state_before_reset=True)
            is False
        )


@pytest.mark.asyncio
async def test_execute_power_on_state_unknown(adapter: MGMTBluetoothCtl) -> None:
    with (
        patch.object(adapter, "set_powered", AsyncMock(return_value=True)),
        patch.object(adapter, "wait_for_power_state", AsyncMock(return_value=None)),
    ):
        assert (
            await recover._execute_power_on(adapter, power_state_before_reset=True)
            is False
        )


@pytest.mark.asyncio
async def test_execute_power_on_set_powered_attribute_error(
    adapter: MGMTBluetoothCtl,
) -> None:
    with patch.object(
        adapter, "set_powered", AsyncMock(side_effect=AttributeError("gone"))
    ):
        assert (
            await recover._execute_power_on(adapter, power_state_before_reset=True)
            is False
        )


# ---------------------------------------------------------------------------
# _execute_power_off
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_execute_power_off_when_on(adapter: MGMTBluetoothCtl) -> None:
    set_powered = AsyncMock(return_value=True)
    with (
        patch.object(adapter, "set_powered", set_powered),
        patch.object(adapter, "wait_for_power_state", AsyncMock(return_value=False)),
    ):
        assert (
            await recover._execute_power_off(adapter, power_state_before_reset=True)
            is True
        )
    set_powered.assert_awaited_once_with(False)


@pytest.mark.asyncio
async def test_execute_power_off_when_off(adapter: MGMTBluetoothCtl) -> None:
    set_powered = AsyncMock()
    with patch.object(adapter, "set_powered", set_powered):
        assert (
            await recover._execute_power_off(adapter, power_state_before_reset=False)
            is True
        )
    set_powered.assert_not_called()


@pytest.mark.asyncio
async def test_execute_power_off_unknown_state(adapter: MGMTBluetoothCtl) -> None:
    set_powered = AsyncMock()
    with patch.object(adapter, "set_powered", set_powered):
        assert (
            await recover._execute_power_off(adapter, power_state_before_reset=None)
            is False
        )


@pytest.mark.asyncio
async def test_execute_power_off_attribute_error(adapter: MGMTBluetoothCtl) -> None:
    with patch.object(
        adapter, "set_powered", AsyncMock(side_effect=AttributeError("gone"))
    ):
        assert (
            await recover._execute_power_off(adapter, power_state_before_reset=True)
            is False
        )


# ---------------------------------------------------------------------------
# _set_adapter_up_down / _bounce_adapter_interface
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_set_adapter_up_down_passes_low_byte(adapter: MGMTBluetoothCtl) -> None:
    adapter.idx = 0
    sock = MagicMock()
    sock.fileno.return_value = 9
    loop = asyncio.get_running_loop()
    with patch.object(recover, "ioctl") as mock_ioctl:
        await recover._set_adapter_up_down(adapter, sock, loop, recover.HCIDEVUP, "up")
    mock_ioctl.assert_called_once_with(9, recover.HCIDEVUP, 0)


@pytest.mark.asyncio
async def test_bounce_adapter_interface_down_then_up(adapter: MGMTBluetoothCtl) -> None:
    sock = MagicMock()
    calls: list[str] = []

    async def fake_set(_adapter, _sock, _loop, code, state):  # noqa: ANN001
        calls.append(state)

    with (
        patch.object(recover, "raw_open", return_value=sock),
        patch.object(recover, "raw_close") as mock_close,
        patch.object(recover, "_set_adapter_up_down", side_effect=fake_set),
        patch.object(recover.asyncio, "sleep", AsyncMock()),
    ):
        await recover._bounce_adapter_interface(adapter, up=True, down=True)

    assert calls == ["down", "up"]
    mock_close.assert_called_once_with(sock)


@pytest.mark.asyncio
async def test_bounce_adapter_interface_up_only(adapter: MGMTBluetoothCtl) -> None:
    sock = MagicMock()
    calls: list[str] = []

    async def fake_set(_adapter, _sock, _loop, code, state):  # noqa: ANN001
        calls.append(state)

    with (
        patch.object(recover, "raw_open", return_value=sock),
        patch.object(recover, "raw_close"),
        patch.object(recover, "_set_adapter_up_down", side_effect=fake_set),
        patch.object(recover.asyncio, "sleep", AsyncMock()),
    ):
        await recover._bounce_adapter_interface(adapter, up=True, down=False)

    assert calls == ["up"]


# ---------------------------------------------------------------------------
# _execute_reset
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_execute_reset_happy_path(adapter: MGMTBluetoothCtl) -> None:
    with (
        patch.object(adapter, "get_powered", AsyncMock(return_value=True)),
        patch.object(recover, "_execute_power_off", AsyncMock(return_value=True)),
        patch.object(recover, "_bounce_adapter_interface", AsyncMock()),
        patch.object(recover, "_execute_power_on", AsyncMock(return_value=True)),
    ):
        assert await recover._execute_reset(adapter) is True


@pytest.mark.asyncio
async def test_execute_reset_power_on_fails(adapter: MGMTBluetoothCtl) -> None:
    with (
        patch.object(adapter, "get_powered", AsyncMock(return_value=True)),
        patch.object(recover, "_execute_power_off", AsyncMock(return_value=True)),
        patch.object(recover, "_bounce_adapter_interface", AsyncMock()),
        patch.object(recover, "_execute_power_on", AsyncMock(return_value=False)),
    ):
        assert await recover._execute_reset(adapter) is False


@pytest.mark.asyncio
async def test_execute_reset_skips_power_off_on_timeout(
    adapter: MGMTBluetoothCtl,
) -> None:
    power_off = AsyncMock(return_value=True)
    with (
        patch.object(
            adapter, "get_powered", AsyncMock(side_effect=asyncio.TimeoutError())
        ),
        patch.object(recover, "_execute_power_off", power_off),
        patch.object(recover, "_bounce_adapter_interface", AsyncMock()),
        patch.object(recover, "_execute_power_on", AsyncMock(return_value=True)),
    ):
        assert await recover._execute_reset(adapter) is True
    # Frozen adapter: power off must be skipped.
    power_off.assert_not_called()


@pytest.mark.asyncio
async def test_execute_reset_final_bounce_already_up(adapter: MGMTBluetoothCtl) -> None:
    async def bounce(_adapter, *, down, up):  # noqa: ANN001
        if down is False and up is True:
            raise OSError(errno.EALREADY, "already up")

    with (
        patch.object(adapter, "get_powered", AsyncMock(return_value=True)),
        patch.object(recover, "_execute_power_off", AsyncMock(return_value=True)),
        patch.object(recover, "_bounce_adapter_interface", side_effect=bounce),
        patch.object(recover, "_execute_power_on", AsyncMock(return_value=True)),
    ):
        assert await recover._execute_reset(adapter) is True


@pytest.mark.asyncio
async def test_execute_reset_final_bounce_oserror(adapter: MGMTBluetoothCtl) -> None:
    async def bounce(_adapter, *, down, up):  # noqa: ANN001
        if down is False and up is True:
            raise OSError(errno.EIO, "io error")

    with (
        patch.object(adapter, "get_powered", AsyncMock(return_value=True)),
        patch.object(recover, "_execute_power_off", AsyncMock(return_value=True)),
        patch.object(recover, "_bounce_adapter_interface", side_effect=bounce),
        patch.object(recover, "_execute_power_on", AsyncMock(return_value=True)),
    ):
        assert await recover._execute_reset(adapter) is False


@pytest.mark.asyncio
async def test_execute_reset_final_bounce_unexpected_error(
    adapter: MGMTBluetoothCtl,
) -> None:
    # A non-OSError raised by the final bounce is swallowed and fails the reset.
    async def bounce(_adapter, *, down, up):  # noqa: ANN001
        if down is False and up is True:
            raise RuntimeError("boom")

    with (
        patch.object(adapter, "get_powered", AsyncMock(return_value=True)),
        patch.object(recover, "_execute_power_off", AsyncMock(return_value=True)),
        patch.object(recover, "_bounce_adapter_interface", side_effect=bounce),
        patch.object(recover, "_execute_power_on", AsyncMock(return_value=True)),
    ):
        assert await recover._execute_reset(adapter) is False


@pytest.mark.asyncio
@pytest.mark.parametrize("exc", [AttributeError("gone"), RuntimeError("unexpected")])
async def test_execute_reset_get_powered_error_continues(
    adapter: MGMTBluetoothCtl, exc: Exception
) -> None:
    # If reading the initial power state fails (but does not time out), the reset
    # still proceeds: power-off is attempted, then bounce + power-on decide.
    power_off = AsyncMock(return_value=True)
    with (
        patch.object(adapter, "get_powered", AsyncMock(side_effect=exc)),
        patch.object(recover, "_execute_power_off", power_off),
        patch.object(recover, "_bounce_adapter_interface", AsyncMock()),
        patch.object(recover, "_execute_power_on", AsyncMock(return_value=True)),
    ):
        assert await recover._execute_reset(adapter) is True
    power_off.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("exc", [asyncio.TimeoutError(), RuntimeError("boom")])
async def test_execute_reset_power_off_error_is_swallowed(
    adapter: MGMTBluetoothCtl, exc: Exception
) -> None:
    # Failures while powering off are swallowed; the reset proceeds to bounce/power-on.
    with (
        patch.object(adapter, "get_powered", AsyncMock(return_value=True)),
        patch.object(recover, "_execute_power_off", AsyncMock(side_effect=exc)),
        patch.object(recover, "_bounce_adapter_interface", AsyncMock()),
        patch.object(recover, "_execute_power_on", AsyncMock(return_value=True)),
    ):
        assert await recover._execute_reset(adapter) is True


@pytest.mark.asyncio
async def test_execute_reset_first_bounce_error_is_swallowed(
    adapter: MGMTBluetoothCtl,
) -> None:
    # The down/up bounce before power-on is best-effort: a failure does not abort.
    async def bounce(_adapter, *, down, up):  # noqa: ANN001
        if down is True:
            raise OSError(errno.EIO, "io error")

    with (
        patch.object(adapter, "get_powered", AsyncMock(return_value=True)),
        patch.object(recover, "_execute_power_off", AsyncMock(return_value=True)),
        patch.object(recover, "_bounce_adapter_interface", side_effect=bounce),
        patch.object(recover, "_execute_power_on", AsyncMock(return_value=True)),
    ):
        assert await recover._execute_reset(adapter) is True


@pytest.mark.asyncio
@pytest.mark.parametrize("exc", [asyncio.TimeoutError(), RuntimeError("boom")])
async def test_execute_reset_power_on_error_fails(
    adapter: MGMTBluetoothCtl, exc: Exception
) -> None:
    # A timeout or unexpected error while powering back on fails the reset.
    with (
        patch.object(adapter, "get_powered", AsyncMock(return_value=True)),
        patch.object(recover, "_execute_power_off", AsyncMock(return_value=True)),
        patch.object(recover, "_bounce_adapter_interface", AsyncMock()),
        patch.object(recover, "_execute_power_on", AsyncMock(side_effect=exc)),
    ):
        assert await recover._execute_reset(adapter) is False


# ---------------------------------------------------------------------------
# raw_open / raw_close
# ---------------------------------------------------------------------------


def test_raw_open_binds_adapter() -> None:
    sock = MagicMock()
    with patch.object(recover.socket, "socket", return_value=sock) as mock_socket:
        result = raw_open(2)
    mock_socket.assert_called_once()
    sock.bind.assert_called_once_with((2,))
    assert result is sock


def test_raw_close_detaches_and_closes() -> None:
    sock = MagicMock()
    sock.detach.return_value = 11
    with patch.object(recover.socket, "close") as mock_close:
        raw_close(sock)
    sock.detach.assert_called_once()
    mock_close.assert_called_once_with(11)


# ---------------------------------------------------------------------------
# _get_adapter context manager
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_adapter_yields_resolved_adapter() -> None:
    ctl = MagicMock()
    ctl.idx = 0
    ctl.hci_name = "hci0"
    ctl.mac = "AA:BB:CC:DD:EE:FF"
    ctl.setup = AsyncMock()
    ctl.close = AsyncMock()
    with patch.object(recover, "MGMTBluetoothCtl", return_value=ctl):
        async with recover._get_adapter("hci0", "AA:BB:CC:DD:EE:FF") as got:
            assert got is ctl
    ctl.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_adapter_yields_none_when_idx_missing() -> None:
    ctl = MagicMock()
    ctl.idx = None
    ctl.setup = AsyncMock()
    ctl.close = AsyncMock()
    with patch.object(recover, "MGMTBluetoothCtl", return_value=ctl):
        async with recover._get_adapter("hci0", "AA:BB:CC:DD:EE:FF") as got:
            assert got is None
    ctl.close.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exc",
    [
        recover.btmgmt_socket.BluetoothSocketError("no socket"),
        OSError("io"),
        asyncio.TimeoutError(),
    ],
)
async def test_get_adapter_yields_none_on_setup_error(exc: Exception) -> None:
    ctl = MagicMock()
    ctl.setup = AsyncMock(side_effect=exc)
    ctl.close = AsyncMock()
    with patch.object(recover, "MGMTBluetoothCtl", return_value=ctl):
        async with recover._get_adapter("hci0", "AA:BB:CC:DD:EE:FF") as got:
            assert got is None


@pytest.mark.asyncio
async def test_get_adapter_timeout_logs_timeout_message(
    caplog: pytest.LogCaptureFixture,
) -> None:
    ctl = MagicMock()
    ctl.setup = AsyncMock(side_effect=asyncio.TimeoutError())
    ctl.close = AsyncMock()
    with (
        patch.object(recover, "MGMTBluetoothCtl", return_value=ctl),
        caplog.at_level(logging.WARNING),
    ):
        async with recover._get_adapter("hci0", "AA:BB:CC:DD:EE:FF") as got:
            assert got is None
    assert "due to timeout" in caplog.text


@pytest.mark.asyncio
async def test_get_adapter_close_failure_is_swallowed() -> None:
    # A failure closing the adapter in the finally block must not propagate.
    ctl = MagicMock()
    ctl.idx = 0
    ctl.hci_name = "hci0"
    ctl.mac = "AA:BB:CC:DD:EE:FF"
    ctl.setup = AsyncMock()
    ctl.close = AsyncMock(side_effect=OSError("close failed"))
    with patch.object(recover, "MGMTBluetoothCtl", return_value=ctl):
        async with recover._get_adapter("hci0", "AA:BB:CC:DD:EE:FF") as got:
            assert got is ctl
    ctl.close.assert_awaited_once()


# ---------------------------------------------------------------------------
# BluetoothMGMTProtocol
# ---------------------------------------------------------------------------


def _make_protocol() -> BluetoothMGMTProtocol:
    loop = asyncio.get_running_loop()
    return BluetoothMGMTProtocol(5, loop.create_future(), MagicMock())


@pytest.mark.asyncio
async def test_protocol_connection_made_resolves_future() -> None:
    proto = _make_protocol()
    transport = MagicMock()
    proto.connection_made(transport)
    assert proto.transport is transport
    assert proto.connection_mode_future.done()


@pytest.mark.asyncio
async def test_protocol_data_received_resolves_future() -> None:
    proto = _make_protocol()
    loop = asyncio.get_running_loop()
    proto.future = loop.create_future()
    response = MagicMock()
    response.cmd_response_frame = MagicMock()
    with patch.object(recover.btmgmt_protocol, "reader", return_value=response):
        proto.data_received(b"payload")
    assert proto.future.result() is response


@pytest.mark.asyncio
async def test_protocol_data_received_ignores_value_error() -> None:
    proto = _make_protocol()
    loop = asyncio.get_running_loop()
    proto.future = loop.create_future()
    with patch.object(
        recover.btmgmt_protocol, "reader", side_effect=ValueError("bad event")
    ):
        proto.data_received(b"payload")
    # Malformed event must not crash or resolve the pending future.
    assert not proto.future.done()


@pytest.mark.asyncio
async def test_protocol_send_without_transport_raises() -> None:
    proto = _make_protocol()
    proto.transport = None
    with patch.object(recover.btmgmt_protocol, "command", return_value=[]):
        with pytest.raises(recover.btmgmt_socket.BluetoothSocketError):
            await proto.send("ReadControllerIndexList", None)


@pytest.mark.asyncio
async def test_protocol_send_writes_to_socket_directly() -> None:
    proto = _make_protocol()
    proto.transport = MagicMock()
    frame = MagicMock()
    frame.octets = b"data"
    with patch.object(recover.btmgmt_protocol, "command", return_value=[frame]):
        task = asyncio.ensure_future(proto.send("SetPowered", 0, 1))
        await asyncio.sleep(0)
        assert proto.future is not None
        proto.future.set_result("RESPONSE")
        result = await task
    # The kernel-ABI workaround writes to the raw socket, not the transport.
    cast(MagicMock, proto.sock).send.assert_called_once_with(b"data")
    cast(MagicMock, proto.transport).write.assert_not_called()
    assert result == "RESPONSE"


@pytest.mark.asyncio
async def test_protocol_send_times_out() -> None:
    proto = _make_protocol()
    proto.timeout = 0.01
    proto.transport = MagicMock()
    frame = MagicMock()
    frame.octets = b"data"
    with patch.object(recover.btmgmt_protocol, "command", return_value=[frame]):
        with pytest.raises(asyncio.TimeoutError):
            await proto.send("ReadControllerInformation", 0)


@pytest.mark.asyncio
async def test_protocol_timeout_future_sets_exception() -> None:
    proto = _make_protocol()
    loop = asyncio.get_running_loop()
    fut = loop.create_future()
    proto._timeout_future(fut)
    with pytest.raises(asyncio.TimeoutError):
        fut.result()


@pytest.mark.asyncio
async def test_protocol_connection_lost_clears_transport() -> None:
    proto = _make_protocol()
    proto.transport = MagicMock()
    proto.connection_lost(OSError("dropped"))
    assert proto.transport is None


# ---------------------------------------------------------------------------
# MGMTBluetoothCtl.setup
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_setup_success() -> None:
    ctl = MGMTBluetoothCtl("hci0", "AA:BB:CC:DD:EE:FF", 5)
    sock = MagicMock()
    loop = asyncio.get_running_loop()

    async def fake_create(sock_arg, factory, *args, **kwargs):  # noqa: ANN001
        proto = factory()
        proto.connection_made(MagicMock())
        return (MagicMock(), proto)

    with (
        patch.object(recover.btmgmt_socket, "open", return_value=sock),
        patch.object(loop, "_create_connection_transport", fake_create),
        patch.object(recover.MGMTBluetoothCtl, "_find_controller", AsyncMock()),
    ):
        await ctl.setup()
    assert ctl.sock is sock
    assert isinstance(ctl.protocol, BluetoothMGMTProtocol)


@pytest.mark.asyncio
async def test_setup_timeout_closes_socket() -> None:
    ctl = MGMTBluetoothCtl("hci0", "AA:BB:CC:DD:EE:FF", 5)
    sock = MagicMock()
    loop = asyncio.get_running_loop()

    async def hang(*args, **kwargs):  # noqa: ANN001
        await asyncio.sleep(10)

    real_timeout = recover.asyncio_timeout

    with (
        patch.object(recover.btmgmt_socket, "open", return_value=sock),
        patch.object(loop, "_create_connection_transport", hang),
        patch.object(recover, "asyncio_timeout", lambda _t: real_timeout(0.01)),
        patch.object(recover.btmgmt_socket, "close") as mock_close,
    ):
        with pytest.raises(asyncio.TimeoutError):
            await ctl.setup()
    mock_close.assert_called_once_with(sock)


# ---------------------------------------------------------------------------
# recover_adapter — top-level state machine
# ---------------------------------------------------------------------------


def _resolved_adapter() -> MagicMock:
    ctl = MagicMock()
    ctl.idx = 0
    ctl.hci_name = "hci0"
    ctl.mac = "AA:BB:CC:DD:EE:FF"
    ctl.name = "hci0 [AA:BB:CC:DD:EE:FF] (0)"
    return ctl


@pytest.mark.asyncio
async def test_recover_adapter_not_found() -> None:
    with patch.object(recover, "_get_adapter", return_value=adapter_cm(None)):
        assert await recover.recover_adapter(0, "AA:BB:CC:DD:EE:FF") is False


@pytest.mark.asyncio
async def test_recover_adapter_power_cycle_success() -> None:
    ctl = _resolved_adapter()
    with (
        patch.object(recover, "_get_adapter", return_value=adapter_cm(ctl)),
        patch.object(recover, "_check_or_unblock_rfkill", AsyncMock(return_value=True)),
        patch.object(recover, "_power_cycle_adapter", AsyncMock(return_value=True)),
        patch.object(recover.asyncio, "sleep", AsyncMock()),
    ):
        # Power cycle succeeds and the adapter has not gone silent: short-circuits True.
        assert await recover.recover_adapter(0, "AA:BB:CC:DD:EE:FF") is True


@pytest.mark.asyncio
async def test_recover_adapter_usb_reset_path() -> None:
    first = _resolved_adapter()
    second = _resolved_adapter()
    with (
        patch.object(
            recover,
            "_get_adapter",
            side_effect=[adapter_cm(first), adapter_cm(second)],
        ),
        patch.object(recover, "_check_or_unblock_rfkill", AsyncMock(return_value=True)),
        patch.object(recover, "_power_cycle_adapter", AsyncMock(return_value=False)),
        patch.object(recover, "_usb_reset_adapter", AsyncMock(return_value=True)),
        patch.object(recover.asyncio, "sleep", AsyncMock()),
    ):
        assert await recover.recover_adapter(0, "AA:BB:CC:DD:EE:FF") is True


@pytest.mark.asyncio
async def test_recover_adapter_usb_reset_fails() -> None:
    ctl = _resolved_adapter()
    with (
        patch.object(recover, "_get_adapter", return_value=adapter_cm(ctl)),
        patch.object(recover, "_check_or_unblock_rfkill", AsyncMock(return_value=True)),
        patch.object(recover, "_power_cycle_adapter", AsyncMock(return_value=False)),
        patch.object(recover, "_usb_reset_adapter", AsyncMock(return_value=False)),
        patch.object(recover.asyncio, "sleep", AsyncMock()),
    ):
        assert await recover.recover_adapter(0, "AA:BB:CC:DD:EE:FF") is False


@pytest.mark.asyncio
async def test_recover_adapter_gone_silent_forces_usb_reset() -> None:
    first = _resolved_adapter()
    second = _resolved_adapter()
    power_cycle = AsyncMock(return_value=True)
    usb_reset = AsyncMock(return_value=True)
    with (
        patch.object(
            recover,
            "_get_adapter",
            side_effect=[adapter_cm(first), adapter_cm(second)],
        ),
        patch.object(recover, "_check_or_unblock_rfkill", AsyncMock(return_value=True)),
        patch.object(recover, "_power_cycle_adapter", power_cycle),
        patch.object(recover, "_usb_reset_adapter", usb_reset),
        patch.object(recover.asyncio, "sleep", AsyncMock()),
    ):
        # gone_silent=True: even a successful power cycle still triggers a USB reset.
        assert (
            await recover.recover_adapter(0, "AA:BB:CC:DD:EE:FF", gone_silent=True)
            is True
        )
    usb_reset.assert_awaited_once()


@pytest.mark.asyncio
async def test_recover_adapter_gone_silent_non_usb_power_cycle_ok() -> None:
    # gone_silent forces a USB reset, but the adapter is not a USB device
    # (USB reset returns None). The power cycle succeeded, so a non-USB adapter
    # is still recovered and recover_adapter must report success.
    ctl = _resolved_adapter()
    with (
        patch.object(recover, "_get_adapter", return_value=adapter_cm(ctl)),
        patch.object(recover, "_check_or_unblock_rfkill", AsyncMock(return_value=True)),
        patch.object(recover, "_power_cycle_adapter", AsyncMock(return_value=True)),
        patch.object(recover, "_usb_reset_adapter", AsyncMock(return_value=None)),
        patch.object(recover.asyncio, "sleep", AsyncMock()),
    ):
        assert (
            await recover.recover_adapter(0, "AA:BB:CC:DD:EE:FF", gone_silent=True)
            is True
        )


@pytest.mark.asyncio
async def test_recover_adapter_non_usb_power_cycle_failed() -> None:
    # USB reset not applicable (None) AND the power cycle failed: nothing
    # recovered the adapter, so recover_adapter must report failure.
    ctl = _resolved_adapter()
    with (
        patch.object(recover, "_get_adapter", return_value=adapter_cm(ctl)),
        patch.object(recover, "_check_or_unblock_rfkill", AsyncMock(return_value=True)),
        patch.object(recover, "_power_cycle_adapter", AsyncMock(return_value=False)),
        patch.object(recover, "_usb_reset_adapter", AsyncMock(return_value=None)),
        patch.object(recover.asyncio, "sleep", AsyncMock()),
    ):
        assert await recover.recover_adapter(0, "AA:BB:CC:DD:EE:FF") is False


@pytest.mark.asyncio
async def test_recover_adapter_second_lookup_fails() -> None:
    first = _resolved_adapter()
    calls = {"n": 0}

    def get_adapter(*_args: object, **_kwargs: object) -> object:
        calls["n"] += 1
        # First lookup (pre-reset) resolves; every post-reset lookup misses.
        return adapter_cm(first if calls["n"] == 1 else None)

    with (
        patch.object(recover, "_get_adapter", side_effect=get_adapter),
        patch.object(recover, "_check_or_unblock_rfkill", AsyncMock(return_value=True)),
        patch.object(recover, "_power_cycle_adapter", AsyncMock(return_value=False)),
        patch.object(recover, "_usb_reset_adapter", AsyncMock(return_value=True)),
        patch.object(recover.asyncio, "sleep", AsyncMock()),
    ):
        # USB reset succeeded but the adapter never reappears: every retry
        # misses, so recovery is reported as failed only after exhausting them.
        assert await recover.recover_adapter(0, "AA:BB:CC:DD:EE:FF") is False

    # Pre-reset lookup + one lookup per post-reset attempt.
    assert calls["n"] == 1 + recover.POST_RESET_LOOKUP_ATTEMPTS


@pytest.mark.asyncio
async def test_recover_adapter_second_lookup_succeeds_after_retry() -> None:
    # The adapter re-enumerates slowly after the USB reset: the first two
    # post-reset lookups miss, then it reappears and recovery succeeds.
    first = _resolved_adapter()
    second = _resolved_adapter()
    sleep = AsyncMock()
    with (
        patch.object(
            recover,
            "_get_adapter",
            side_effect=[
                adapter_cm(first),
                adapter_cm(None),
                adapter_cm(None),
                adapter_cm(second),
            ],
        ),
        patch.object(recover, "_check_or_unblock_rfkill", AsyncMock(return_value=True)),
        patch.object(recover, "_power_cycle_adapter", AsyncMock(return_value=False)),
        patch.object(recover, "_usb_reset_adapter", AsyncMock(return_value=True)),
        patch.object(recover.asyncio, "sleep", sleep),
    ):
        assert await recover.recover_adapter(0, "AA:BB:CC:DD:EE:FF") is True

    # Exact sleep sequence: the post-USB-reset DBUS_REGISTER_TIME wait, then one
    # POST_RESET_LOOKUP_RETRY_TIME wait per missed lookup (two misses here)
    # before the adapter is found on the third attempt.
    assert sleep.await_args_list == [
        call(recover.DBUS_REGISTER_TIME),
        call(recover.POST_RESET_LOOKUP_RETRY_TIME),
        call(recover.POST_RESET_LOOKUP_RETRY_TIME),
    ]


@pytest.mark.asyncio
async def test_recover_adapter_handles_moved_hci_and_resolved_mac() -> None:
    # Adapter reports a different hci number and MAC than requested.
    ctl = MagicMock()
    ctl.idx = 1
    ctl.hci_name = "hci1"
    ctl.mac = "11:22:33:44:55:66"
    ctl.name = "hci1 [11:22:33:44:55:66] (1)"
    with (
        patch.object(recover, "_get_adapter", return_value=adapter_cm(ctl)),
        patch.object(recover, "_check_or_unblock_rfkill", AsyncMock(return_value=True)),
        patch.object(recover, "_power_cycle_adapter", AsyncMock(return_value=True)),
        patch.object(recover.asyncio, "sleep", AsyncMock()),
    ):
        assert await recover.recover_adapter(0, "AA:BB:CC:DD:EE:FF") is True


@pytest.mark.asyncio
async def test_recover_adapter_first_rfkill_block_is_non_fatal() -> None:
    # A failed rfkill unblock before the power cycle only warns; it does not abort.
    ctl = _resolved_adapter()
    with (
        patch.object(recover, "_get_adapter", return_value=adapter_cm(ctl)),
        patch.object(
            recover, "_check_or_unblock_rfkill", AsyncMock(return_value=False)
        ),
        patch.object(recover, "_power_cycle_adapter", AsyncMock(return_value=True)),
        patch.object(recover.asyncio, "sleep", AsyncMock()),
    ):
        assert await recover.recover_adapter(0, "AA:BB:CC:DD:EE:FF") is True


@pytest.mark.asyncio
async def test_recover_adapter_post_reset_rfkill_blocked() -> None:
    first = _resolved_adapter()
    second = _resolved_adapter()
    with (
        patch.object(
            recover,
            "_get_adapter",
            side_effect=[adapter_cm(first), adapter_cm(second)],
        ),
        # Passes the first rfkill check, fails the post-reset one.
        patch.object(
            recover,
            "_check_or_unblock_rfkill",
            AsyncMock(side_effect=[True, False]),
        ),
        patch.object(recover, "_power_cycle_adapter", AsyncMock(return_value=False)),
        patch.object(recover, "_usb_reset_adapter", AsyncMock(return_value=True)),
        patch.object(recover.asyncio, "sleep", AsyncMock()),
    ):
        assert await recover.recover_adapter(0, "AA:BB:CC:DD:EE:FF") is False


@pytest.mark.asyncio
async def test_recover_adapter_post_reset_moved_hci() -> None:
    # The USB reset moves the adapter to a new hci number: the post-reset
    # lookup resolves it under hci1, and recovery still succeeds.
    first = _resolved_adapter()
    moved = MagicMock()
    moved.idx = 1
    moved.hci_name = "hci1"
    moved.mac = "AA:BB:CC:DD:EE:FF"
    moved.name = "hci1 [AA:BB:CC:DD:EE:FF] (1)"
    with (
        patch.object(
            recover,
            "_get_adapter",
            side_effect=[adapter_cm(first), adapter_cm(moved)],
        ),
        patch.object(recover, "_check_or_unblock_rfkill", AsyncMock(return_value=True)),
        patch.object(recover, "_power_cycle_adapter", AsyncMock(return_value=False)),
        patch.object(recover, "_usb_reset_adapter", AsyncMock(return_value=True)),
        patch.object(recover.asyncio, "sleep", AsyncMock()),
    ):
        assert await recover.recover_adapter(0, "AA:BB:CC:DD:EE:FF") is True
