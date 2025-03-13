# Changelog

<!--next-version-placeholder-->

## v1.4.5 (2025-03-13)

### Fix

* Downgrade power on success log message to debug ([#83](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/83)) ([`da6ca83`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/da6ca83c1c55b4c154b46b18afacbf3ab7d9b063))

## v1.4.4 (2025-02-19)

### Fix

* Handle case where adapter moves to index 0 after USB reset ([#79](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/79)) ([`34517d3`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/34517d37e426cba26cceb0bcdc8da2f98e63610b))

## v1.4.3 (2025-02-19)

### Fix

* Rfkill unblocking when adapter idx is 0 ([#78](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/78)) ([`f6dbba0`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/f6dbba060307aca0657ce6a967153c2e373b6aaa))

## v1.4.2 (2024-04-25)

### Fix

* Ensure timeout does not raise cancellation ([#46](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/46)) ([`4575fdd`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/4575fdd52778e09dee5e6bce51e7636e9609aaac))

## v1.4.1 (2024-04-18)

### Fix

* Wait for connection made ([#45](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/45)) ([`70aa8df`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/70aa8df23ac7a604177af680b63fdb1f00e430b8))

## v1.4.0 (2024-03-13)

### Feature

* Only import recovery code the first time the recovery is called ([#44](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/44)) ([`39372f0`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/39372f085e624a7fba8d06ed1ddc8a4a52c7bb7c))

## v1.3.0 (2024-01-10)

### Feature

* Ensure library can be loaded on windows ([#43](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/43)) ([`dd234f8`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/dd234f847c54fe8471b51378ab03b2d1a9f2f497))

## v1.2.3 (2023-09-09)

### Fix

* Add missing async keyword to send timeout ([#42](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/42)) ([`1097e44`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/1097e44a8c6051aeb6e9f4d53631c8ecf1e47d54))

## v1.2.2 (2023-09-07)

### Fix

* Ensure timeouts work with py3.11 ([#41](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/41)) ([`99b9f48`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/99b9f48f8f742d6004720b26e25b9c1f6cd455e7))

## v1.2.1 (2023-07-12)

### Fix

* Make MGMTBluetoothCtl aware of down adapters ([#38](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/38)) ([`3c6bc12`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/3c6bc12e021611590e13c400aeedc665b582a9c3))

## v1.2.0 (2023-05-10)
### Feature
* Try to bounce the adapter if setting power state fails ([#36](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/36)) ([`11ec5e2`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/11ec5e2e5b8fc8e6d58d9b822dc333dbf89e6952))

## v1.1.2 (2023-05-04)
### Fix
* Proceed with reset when getting power state times out ([#34](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/34)) ([`aae8c84`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/aae8c848fb894686ba1076d395b402701b0cedc5))

## v1.1.1 (2023-05-03)
### Fix
* Pass on event types we do not know how to process ([#33](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/33)) ([`2bbca73`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/2bbca73867f6bbd599544fe47ff6b0c468c6436a))

## v1.1.0 (2023-05-03)
### Feature
* Do a down/up on the interface when resetting the adapter ([#31](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/31)) ([`ae3f63b`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/ae3f63b0b13672df6375e4c6ee5514439484a31f))

## v1.0.3 (2022-12-15)
### Fix
* Handle the btsocket being closed out from under us ([#29](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/29)) ([`1e0d878`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/1e0d87853379e1ca89b50ecd9698e8c61c37e398))

## v1.0.2 (2022-12-15)
### Fix
* Handle the case where a btsocket cannot be created ([#28](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/28)) ([`6e8e8e1`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/6e8e8e1b0b42a0c830a70cafafd8a25e3df631d5))

## v1.0.1 (2022-12-15)
### Fix
* Handle adapter moving to a new hci number after reset ([#27](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/27)) ([`662f710`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/662f710c30b07a0904cc9a3d00b39303ee43db4a))

## v1.0.0 (2022-12-12)
### Feature
* Add support for being able to reset the adapter by mac address when the hci interface is lost ([#26](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/issues/26)) ([`72d6114`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/72d6114a4c6b553fb574f43fc793fd0c7a969521))

### Breaking
* The mac address must now be passed to `recover_adapter` ([`72d6114`](https://github.com/Bluetooth-Devices/bluetooth-auto-recovery/commit/72d6114a4c6b553fb574f43fc793fd0c7a969521))

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
