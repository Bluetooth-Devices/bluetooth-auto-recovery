"""Automatic recovery for bluetooth adapters."""
from __future__ import annotations

import asyncio
import logging

import async_timeout
import pyric.utils.rfkill as rfkill
from btsocket import btmgmt_protocol, btmgmt_sync

_LOGGER = logging.getLogger(__name__)

POWER_OFF_TIME = 2
POWER_ON_TIME = 3
MAX_RESET_TIME = 10
DBUS_REGISTER_TIME = 0.5


def rfkill_list_bluetooth(hci: int) -> tuple[bool | None, bool | None]:
    """Execute the rfkill list bluetooth command."""
    hci_idx = f"hci{hci}"
    rfkill_dict = rfkill.rfkill_list()
    try:
        rfkill_hci_state = rfkill_dict[hci_idx]
    except KeyError:
        _LOGGER.error(
            "RF kill switch check failed - no data for %s. Available data: %s",
            hci_idx,
            rfkill_dict,
        )
        return None, None
    soft_block = rfkill_hci_state["soft"]
    hard_block = rfkill_hci_state["hard"]
    return soft_block, hard_block


class MGMTBluetoothCtl:
    """Class to control interfaces using the BlueZ management API"""

    def __init__(self, hci: int) -> None:
        """Initialize the control class."""
        self.idx: int | None = None
        self.mac: str | None = None
        self._hci = hci
        self.presented_list = {}
        idxdata = btmgmt_sync.send("ReadControllerIndexList", None)
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
            hci_info = btmgmt_sync.send("ReadControllerInformation", idx)
            _LOGGER.debug(hci_info)
            # bit 9 == LE capability (https://github.com/bluez/bluez/blob/master/doc/mgmt-api.txt)
            bt_le = bool(
                hci_info.cmd_response_frame.supported_settings & 0b000000001000000000
            )
            if bt_le is not True:
                _LOGGER.warning(
                    "hci%i (%s) have no BT LE capabilities and will be ignored.",
                    idx,
                    hci_info.cmd_response_frame.address,
                )
                continue
            self.presented_list[idx] = hci_info.cmd_response_frame.address
            if hci == idx:
                self.idx = idx
                self.mac = hci_info.cmd_response_frame.address

    def get_powered(self) -> bool | None:
        """Powered state of the interface."""
        if self.idx is not None:
            response = btmgmt_sync.send("ReadControllerInformation", self.idx)
            return response.cmd_response_frame.current_settings.get(
                btmgmt_protocol.SupportedSettings.Powered
            )
        return None

    def set_powered(self, new_state: bool) -> bool:
        """Set the powered state of the interface."""
        response = btmgmt_sync.send("SetPowered", self.idx, int(new_state is True))
        if response.event_frame.status.value == 0x00:  # 0x00 - Success
            return True
        return False


async def _wait_for_power_state(
    loop: asyncio.AbstractEventLoop,
    adapter: MGMTBluetoothCtl,
    new_state: bool,
    timeout: float,
) -> bool | None:
    """Wait for the adapter to be powered on or off."""
    current_state: bool | None = not new_state
    try:
        async with async_timeout.timeout(timeout):
            while True:
                current_state = await loop.run_in_executor(None, adapter.get_powered)
                if current_state == new_state:
                    return current_state
                await asyncio.sleep(0.1)
    except asyncio.TimeoutError:
        return current_state


async def _reset_bluetooth(hci: int) -> bool:
    """Resetting the Bluetooth adapter."""
    _LOGGER.debug("Power cycling Bluetooth adapter hci%i", hci)
    loop = asyncio.get_running_loop()

    soft_block, hard_block = await loop.run_in_executor(
        None, rfkill_list_bluetooth, hci
    )
    if soft_block is True:
        _LOGGER.warning("Bluetooth adapter hci%i is soft blocked by rfkill!", hci)
        return False
    if hard_block is True:
        _LOGGER.warning("Bluetooth adapter hci%i is hard blocked by rfkill!", hci)
        return False

    adapter: MGMTBluetoothCtl = await loop.run_in_executor(None, MGMTBluetoothCtl, hci)

    if adapter.mac is None:
        _LOGGER.error(
            "hci%i seems not to exist (anymore), check BT interface mac address in your settings; "
            "Available adapters: %s ",
            hci,
            adapter.presented_list,
        )
        return False

    pstate_before = await loop.run_in_executor(None, adapter.get_powered)
    if pstate_before is True:
        _LOGGER.debug("Current power state of bluetooth adapter is ON.")
        loop.run_in_executor(None, adapter.set_powered, False)
        await _wait_for_power_state(loop, adapter, False, POWER_OFF_TIME)
    elif pstate_before is False:
        _LOGGER.debug(
            "Current power state of bluetooth adapter hci%i is OFF, trying to turn it back ON",
            hci,
        )
    else:
        _LOGGER.debug("Power state of bluetooth adapter could not be determined")
        return False

    loop.run_in_executor(None, adapter.set_powered, True)
    pstate_after = await _wait_for_power_state(loop, adapter, True, POWER_ON_TIME)

    # Check the state after the reset
    if pstate_after is True:
        if pstate_before is False:
            _LOGGER.warning("Bluetooth adapter hci%i successfully turned back ON", hci)
        else:
            _LOGGER.debug(
                "Power state of bluetooth adapter hci%i is ON after power cycle", hci
            )
        # Give Dbus some time to catch up
        await asyncio.sleep(DBUS_REGISTER_TIME)
        return True

    if pstate_after is False:
        _LOGGER.warning(
            "Power state of bluetooth adapter hci%i is OFF after power cycle", hci
        )
        return False

    _LOGGER.debug(
        "Power state of bluetooth adapter hci%i  could not be determined after power cycle",
        hci,
    )
    return False


async def recover_adapter(hci: int) -> bool:
    """Reset the bluetooth adapter."""
    try:
        async with async_timeout.timeout(MAX_RESET_TIME):
            return await _reset_bluetooth(hci)
    except asyncio.TimeoutError:
        _LOGGER.warning("Reset of hci%i timed out after %s!", hci, MAX_RESET_TIME)
    return False
