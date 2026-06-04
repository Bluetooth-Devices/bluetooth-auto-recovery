# Usage

`bluetooth-auto-recovery` recovers Bluetooth adapters that have stopped
responding ("stuck" adapters). It exposes a single coroutine,
`recover_adapter`.

## Quick start

```python
import asyncio

from bluetooth_auto_recovery import recover_adapter


async def main() -> None:
    # hci0 with the adapter's MAC address.
    recovered = await recover_adapter(0, "00:11:22:33:44:55")
    if recovered:
        print("Adapter recovered")
    else:
        print("Adapter could not be recovered")


asyncio.run(main())
```

## API

```python
async def recover_adapter(hci: int, mac: str, gone_silent: bool = False) -> bool
```

### Parameters

- **`hci`** (`int`) — the adapter's HCI index, e.g. `0` for `hci0`.
- **`mac`** (`str`) — the adapter's MAC address. Case-insensitive; it is
  upper-cased internally.
- **`gone_silent`** (`bool`, default `False`) — set to `True` when the adapter
  is still present but has stopped emitting any events (it has "gone silent").
  A silent adapter is escalated more aggressively: a USB reset is attempted
  even when the power cycle succeeded, because a silent-but-powered adapter is
  not actually working.

### Return value

Returns `True` if the adapter was recovered, `False` otherwise. The call is
best-effort and does not raise for the expected hardware-failure cases — a
`False` return means recovery was attempted but did not succeed.

```{note}
Recovery operations (power cycling, rfkill unblocking, USB reset) typically
require elevated privileges. Run the host process as root or grant it the
relevant `CAP_NET_ADMIN` / device-access capabilities, otherwise the recovery
steps cannot take effect.
```

## How recovery works

`recover_adapter` runs an escalating sequence and stops as soon as the adapter
is healthy again:

1. **rfkill unblock** — if the adapter is soft/hard blocked by rfkill, it is
   unblocked. The result is polled (rather than waiting a single fixed delay)
   so a slow unblock still counts as success.
2. **Power cycle** — the adapter is powered off and back on via the management
   socket. If the adapter has **not** gone silent, a successful power cycle is
   sufficient and the function returns `True`.
3. **USB reset** — if the adapter went silent (or the power cycle failed) and
   the adapter is a USB device, a USB-level reset is issued. This disconnects
   and re-enumerates the adapter, which may also move it to a new HCI index.
   A non-USB adapter (for example a built-in UART controller) cannot be USB
   reset, so recovery falls back to the power-cycle result.
4. **Re-discovery** — after a USB reset the adapter is polled for until it
   re-appears (re-enumeration plus BlueZ re-registration can be slow on devices
   such as a Raspberry Pi or Home Assistant host), following it to its new HCI
   index and clearing rfkill again if needed.

The waits between steps give the kernel and D-Bus time to catch up; on slower
hosts the steps that re-enumerate hardware are polled rather than blocked on a
single fixed timeout.
