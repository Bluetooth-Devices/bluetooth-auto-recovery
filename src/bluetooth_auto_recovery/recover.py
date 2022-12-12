"""Automatic recovery for bluetooth adapters."""
from __future__ import annotations

import asyncio
import logging
import socket
from types import TracebackType
from typing import Any, cast

import async_timeout
import pyric.utils.rfkill as rfkill
from btsocket import btmgmt_protocol, btmgmt_socket
from usb_devices import BluetoothDevice, NotAUSBDeviceError

_LOGGER = logging.getLogger(__name__)

POWER_OFF_TIME = 2
POWER_ON_TIME = 3
MAX_RFKILL_TIME = 3
DBUS_REGISTER_TIME = 1.0

MGMT_PROTOCOL_TIMEOUT = 5


def rfkill_list_bluetooth(hci: int) -> tuple[bool | None, bool | None]:
    """Execute the rfkill list bluetooth command."""
    hci_idx = f"hci{hci}"
    try:
        rfkill_dict = rfkill.rfkill_list()
    except FileNotFoundError as ex:
        _LOGGER.debug(
            "rfkill at /dev/rfkill is not accessible, cannot check bluetooth adapter %s: %s",
            hci_idx,
            ex,
        )
        return None, None
    except IndexError as ex:
        _LOGGER.debug(
            "rfkill at /dev/rfkill returned unexpected results, cannot check bluetooth adapter %s: %s",
            hci_idx,
            ex,
        )
        return None, None
    except PermissionError as ex:
        _LOGGER.debug(
            "Access to rfkill at /dev/rfkill is not permitted, cannot check bluetooth adapter %s: %s",
            hci_idx,
            ex,
        )
        return None, None
    except UnicodeDecodeError as ex:
        _LOGGER.debug(
            "RF kill switch check failed - data for %s is not UTF-8 encoded: %s",
            hci_idx,
            ex,
        )
        return None, None
    except Exception:  # pylint: disable=broad-except
        _LOGGER.exception("RF kill switch check failed")
        return None, None
    try:
        rfkill_hci_state = rfkill_dict[hci_idx]
    except KeyError:
        _LOGGER.debug(
            "RF kill switch check failed - no data for %s. Available data: %s",
            hci_idx,
            rfkill_dict,
        )
        return None, None
    return rfkill_hci_state["soft"], rfkill_hci_state["hard"]


class BluetoothMGMTProtocol(asyncio.Protocol):
    """Bluetooth MGMT protocol."""

    def __init__(self, timeout: float) -> None:
        """Initialize the protocol."""
        self.future: asyncio.Future[btmgmt_protocol.Response] | None = None
        self.transport: asyncio.Transport | None = None
        self.timeout = timeout

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        """Handle connection made."""
        self.transport = cast(asyncio.Transport, transport)

    def data_received(self, data: bytes) -> None:
        """Handle data received."""
        if (
            self.future
            and not self.future.done()
            and (response := btmgmt_protocol.reader(data))
            and response.cmd_response_frame
        ):
            self.future.set_result(response)

    async def send(self, *args: Any) -> btmgmt_protocol.Response:
        """Send command."""
        pkt_objs = btmgmt_protocol.command(*args)
        full_pkt = b""
        for frame in pkt_objs:
            if frame:
                full_pkt += frame.octets
        self.future = asyncio.Future()
        assert self.transport is not None  # nosec
        self.transport.write(full_pkt)
        with async_timeout.timeout(self.timeout):
            return await self.future

    def connection_lost(self, exc: Exception | None) -> None:
        """Handle connection lost."""
        if exc:
            _LOGGER.warning("Bluetooth management socket connection lost: %s", exc)
        self.transport = None


class MGMTBluetoothCtl:
    """Class to control interfaces using the BlueZ management API"""

    def __init__(self, hci: int, mac: str, timeout: float) -> None:
        """Initialize the control class."""
        self.idx: int | None = None
        self.mac = mac
        self.hci = hci
        self.timeout = timeout
        self.protocol: BluetoothMGMTProtocol | None = None
        self.presented_list: dict[int, str] = {}
        self.sock: socket.socket | None = None

    async def __aenter__(self) -> MGMTBluetoothCtl:
        """Enter the context manager."""
        await self._setup()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the context manager."""
        await self._close()

    async def _close(self) -> None:
        """Close the management interface."""
        if self.protocol and self.protocol.transport:
            self.protocol.transport.close()
            self.protocol = None
        btmgmt_socket.close(self.sock)

    async def _setup(self) -> None:
        """Set up management interface."""
        self.sock = btmgmt_socket.open()
        loop = asyncio.get_running_loop()
        try:
            async with async_timeout.timeout(5):
                # _create_connection_transport accessed directly to avoid SOCK_STREAM check
                # see https://bugs.python.org/issue38285
                _, protocol = await loop._create_connection_transport(  # type: ignore[attr-defined]
                    self.sock,
                    lambda: BluetoothMGMTProtocol(self.timeout),
                    None,
                    None,
                )
        except asyncio.TimeoutError:
            btmgmt_socket.close(self.sock)
            raise
        assert isinstance(protocol, BluetoothMGMTProtocol)  # nosec
        self.protocol = protocol
        await self._find_controller()

    async def _find_controller(self) -> None:
        """Find the controller."""
        assert self.protocol is not None  # nosec
        idxdata = await self.protocol.send("ReadControllerIndexList", None)
        if idxdata.event_frame.status.value != 0x00:  # 0x00 - Success
            _LOGGER.error(
                "Unable to get hci controllers index list! Event frame status: %s",
                idxdata.event_frame.status,
            )
            return
        if idxdata.cmd_response_frame.num_controllers == 0:
            _LOGGER.warning("There are no BT controllers present in the system!")
            return
        hci_idx_list = getattr(idxdata.cmd_response_frame, "controller_index[i]")
        for idx in hci_idx_list:
            hci_info = await self.protocol.send("ReadControllerInformation", idx)
            _LOGGER.debug(hci_info)
            mac = hci_info.cmd_response_frame.address
            self.presented_list[idx] = mac
            if self.mac == mac:
                self.idx = idx
                return
        if not self.idx and self.hci in self.presented_list:
            _LOGGER.warning(
                "The mac address %s was not found in the adapter list: %s, "
                "falling back to matching by hci%i",
                self.mac,
                self.presented_list,
                self.hci,
            )
            self.idx = self.hci

    async def get_powered(self) -> bool | None:
        """Powered state of the interface."""
        assert self.protocol is not None  # nosec
        if self.idx is not None:
            response = await self.protocol.send("ReadControllerInformation", self.idx)
            return response.cmd_response_frame.current_settings.get(
                btmgmt_protocol.SupportedSettings.Powered
            )
        return None

    async def set_powered(self, new_state: bool) -> bool:
        """Set the powered state of the interface."""
        assert self.protocol is not None  # nosec
        response = await self.protocol.send(
            "SetPowered", self.idx, int(new_state is True)
        )
        if response.event_frame.status.value == 0x00:  # 0x00 - Success
            return True
        return False

    async def wait_for_power_state(
        self, new_state: bool, timeout: float
    ) -> bool | None:
        """Wait for the adapter to be powered on or off."""
        assert self.protocol is not None  # nosec
        current_state: bool | None = not new_state
        try:
            async with async_timeout.timeout(timeout):
                while True:
                    current_state = await self.get_powered()
                    if current_state == new_state:
                        return current_state
                    await asyncio.sleep(0.1)
        except asyncio.TimeoutError:
            return current_state


async def recover_adapter(hci: int, mac: str) -> bool:
    """Reset the bluetooth adapter."""
    mac = mac.upper()
    _LOGGER.debug(
        "Attempting to recover bluetooth adapter hci%i with mac address %s", hci, mac
    )
    loop = asyncio.get_running_loop()
    try:
        async with async_timeout.timeout(MAX_RFKILL_TIME):
            soft_block, hard_block = await loop.run_in_executor(
                None, rfkill_list_bluetooth, hci
            )
    except asyncio.TimeoutError:
        _LOGGER.warning(
            "Checking rfkill for hci%i timed out after %s seconds!",
            hci,
            MAX_RFKILL_TIME,
        )
    else:
        if soft_block is True:
            _LOGGER.warning("Bluetooth adapter hci%i is soft blocked by rfkill!", hci)
            return False
        if hard_block is True:
            _LOGGER.warning("Bluetooth adapter hci%i is hard blocked by rfkill!", hci)
            return False

    if await _power_cycle_adapter(hci, mac) or await _usb_reset_adapter(hci):
        # Give Dbus some time to catch up
        await asyncio.sleep(DBUS_REGISTER_TIME)
        return True

    return False


async def _power_cycle_adapter(hci: int, mac: str) -> bool:
    name = f"hci{hci} [{mac}]"
    _LOGGER.debug("Attempting to power cycle bluetooth adapter %s", name)
    try:
        async with MGMTBluetoothCtl(hci, mac, MGMT_PROTOCOL_TIMEOUT) as adapter:
            return await _execute_reset(adapter)
    except btmgmt_socket.BluetoothSocketError as ex:
        _LOGGER.warning(
            "Bluetooth adapter %s could not be reset "
            "because the system cannot create a bluetooth socket: %s",
            name,
            ex,
        )
        return False
    except OSError as ex:
        _LOGGER.warning("Bluetooth adapter %s could not be reset: %s", name, ex)
        return False
    except asyncio.TimeoutError:
        _LOGGER.warning("Bluetooth adapter %s could not be reset due to timeout", name)
        return False


async def _usb_reset_adapter(hci: int) -> bool:
    """Reset the bluetooth adapter."""
    _LOGGER.debug("Executing USB reset for Bluetooth adapter hci%i", hci)
    dev = BluetoothDevice(hci)
    try:
        return await dev.async_reset()
    except NotAUSBDeviceError as ex:
        _LOGGER.debug(
            "hci%s is not a USB devices while attempting USB reset: %s", hci, ex
        )
        return False
    except FileNotFoundError as ex:
        _LOGGER.debug("hci%s not found while attempting USB reset: %s", hci, ex)
        return False
    except PermissionError as ex:
        _LOGGER.info(
            "hci%s permission denied to %s while attempting USB reset: %s",
            hci,
            ex.filename,
            ex,
        )
        return False
    except Exception as ex:  # pylint: disable=broad-except
        _LOGGER.exception(
            "Unexpected error while attempting USB reset of hci%s: %s", hci, ex
        )
        return False


async def _execute_reset(adapter: MGMTBluetoothCtl) -> bool:
    """Execute the reset."""
    name = f"hci{adapter.hci} [{adapter.mac}]"
    if adapter.idx is None:
        _LOGGER.error(
            "%s seems not to exist (anymore), check BT interface mac address in your settings; "
            "Available adapters: %s ",
            name,
            adapter.presented_list,
        )
        return False

    try:
        pstate_before = await adapter.get_powered()
    except AttributeError as ex:
        _LOGGER.warning(
            "Could not determine the power state of the Bluetooth adapter %s: %s",
            name,
            ex,
        )
        return False

    if pstate_before is True:
        _LOGGER.debug("Current power state of bluetooth adapter is ON.")
        try:
            await adapter.set_powered(False)
        except AttributeError as ex:
            _LOGGER.warning(
                "Could not power cycle the Bluetooth adapter %s: %s", name, ex
            )
            return False
        await adapter.wait_for_power_state(False, POWER_OFF_TIME)
    elif pstate_before is False:
        _LOGGER.debug(
            "Current power state of bluetooth adapter %s is OFF, trying to turn it back ON",
            name,
        )
    else:
        _LOGGER.debug("Power state of bluetooth adapter could not be determined")
        return False

    try:
        await adapter.set_powered(True)
    except AttributeError as ex:
        _LOGGER.warning(
            "Could not re-enable power after cycle of the Bluetooth adapter %s: %s",
            name,
            ex,
        )
        return False

    pstate_after = await adapter.wait_for_power_state(True, POWER_ON_TIME)

    # Check the state after the reset
    if pstate_after is True:
        if pstate_before is False:
            _LOGGER.warning("Bluetooth adapter %s successfully turned back ON", name)
        else:
            _LOGGER.debug(
                "Power state of bluetooth adapter %s is ON after power cycle", name
            )
        return True

    if pstate_after is False:
        _LOGGER.warning(
            "Power state of bluetooth adapter %s is OFF after power cycle", name
        )
        return False

    _LOGGER.debug(
        "Power state of bluetooth adapter %s could not be determined after power cycle",
        name,
    )
    return False
