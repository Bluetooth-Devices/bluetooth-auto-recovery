# Changelog

<!--next-version-placeholder-->

## v0.5.5 (2022-12-09)
### Fix
* Handle BluetoothSocketError and fallback to usb reset ([#25](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/25)) ([`5d6d1c3`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/5d6d1c390279fbe712f6330f8997dc87f981d5e7))

## v0.5.4 (2022-12-02)
### Fix
* Downgrade permission denied error logging when attempting usb reset ([#24](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/24)) ([`79cf457`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/79cf457f38071ba8265864c8b18acda184065f97))

## v0.5.3 (2022-11-29)
### Fix
* For rfkill not being readable ([#23](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/23)) ([`6c168a0`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/6c168a0704401d6dfcd95ade31b2df47cee03060))

## v0.5.2 (2022-11-27)
### Fix
* Ensure dbus wait always happens on success case ([#22](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/22)) ([`df8e7e0`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/df8e7e0647dd63aa173d8e815b6a5cbfaf40ff41))

## v0.5.1 (2022-11-27)
### Fix
* Bump usb-devices ([#21](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/21)) ([`06c2d05`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/06c2d05f530965fee9a7ea7d0cf3596ba65bddfe))

## v0.5.0 (2022-11-27)
### Feature
* Implement generic usb reset ([#20](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/20)) ([`0d7f045`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/0d7f045703b192b0aa86de482d128a43f48e84bf))

## v0.4.0 (2022-11-16)
### Feature
* Reduce overhead to find a response ([#18](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/18)) ([`219d3f7`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/219d3f77d20415c22412872a24896adee8eefb8e))

## v0.3.6 (2022-10-19)
### Fix
* Soft_block and hard_block were unbound when rfkill fails ([#15](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/15)) ([`9d2aa1a`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/9d2aa1a5245ceef07ecb0f1cbdf668782ff5ec81))

## v0.3.5 (2022-10-19)
### Fix
* Missing param in format string for rfkill timeout message ([#13](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/13)) ([`0022d8a`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/0022d8a28849f51abdc055e6cc1b3c19cbe6abdf))

## v0.3.4 (2022-10-10)
### Fix
* Ensure management socket is closed on failure to prevent a leak ([#12](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/12)) ([`4ab673f`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/4ab673fb989ae696327150337a4dfd4d1770ca9d))

## v0.3.3 (2022-09-11)
### Fix
* Downgrade rfkill check logging to debug ([#11](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/11)) ([`80471e6`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/80471e6155d9d72a2ffa467d580aec4315968aaf))

## v0.3.2 (2022-09-08)
### Fix
* Downgrade rfkill check logging to debug ([#10](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/10)) ([`c7b9539`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/c7b95396c78e9d05a78ce1b9022c481f30a2b9e0))

## v0.3.1 (2022-09-06)
### Fix
* Handle invalid data in rfkill ([#9](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/9)) ([`31c1480`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/31c148013721b22f01d9a107d01a6d6cc576c815))

## v0.3.0 (2022-08-30)
### Feature
* Handle no permission to check rfkill ([#8](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/8)) ([`fcda90d`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/fcda90dcdd104608fb2db4b9feca90a7b0e5c8d5))

## v0.2.2 (2022-08-20)
### Fix
* Give Dbus a bit more time to catch up if the adapter has been recovered ([#7](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/7)) ([`216ef1f`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/216ef1fd0e9ec4ed3b022f9f194282d7b2b359cf))

## v0.2.1 (2022-08-20)
### Fix
* Handle libc.so.6 missing ([#6](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/6)) ([`0d9f4cb`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/0d9f4cbc9bf2a422c2f7a889354b76cfe7c75620))
* Handle rfkill not being available in the container ([#5](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/5)) ([`7736c35`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/7736c35279351c8877514f3324f7428447bdaaea))

## v0.2.0 (2022-08-20)
### Feature
* Give DBus some time to catch up to avoid spurious warnings ([#4](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/4)) ([`63188f6`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/63188f694b667ce5418736f5ca02db8484bc83b9))

## v0.1.0 (2022-08-19)
### Feature
* First release ([#3](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/3)) ([`0109dde`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/0109dde7631e6c4e0b96733e37be8a98beae1822))
