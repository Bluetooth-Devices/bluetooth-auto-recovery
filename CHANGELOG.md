# Changelog

<!--next-version-placeholder-->

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
