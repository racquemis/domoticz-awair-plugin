# Domoticz Awair Element Air Quality Plugin
This is a hardware plugin to import air quality data from Awair Element devices into Domoticz.

Installation
----------------------
```bash
cd domoticz/plugins
git clone https://github.com/racquemis/domoticz-awair-plugin.git
```

Restart your Domoticz service with:

```bash
sudo service domoticz.sh restart
```
Setup
----------------------
If not already done, setup the Awair Element device using the Awair Home App.
Locate the device in the DHCP table of your router or DHCP server, take note of it's IP-Address and add a DHCP reservation for the device.

the local API on the Awair Element device has to be enabled to use the plugin.This can be done from the Awair Home app:
1. Press the Awair+ tab in the lower right-hand corner of the Awair Home App
2. Locate and press "Awair APIs Beta"
3. Select "Local API" in the Awair APIs menu
4. Press "Enable Local API"

Go to **Setup**, **Hardware** in the Domoticz interface and add:
**Awair Element Air Quality**.
Fill in the IP-Address of the device and save.
The plugin should add several new devices to domoticz and start querying the device

Features
----------------------
The plugin adds the following devices to domoticz:
- Awair Air Quality Score [0-100%]
- Temperature/Humidity [°C/%]
- CO2 Level [%]
- VOC Level [ppb]
- PM2.5 Level [µg/m³]
- PM10 Estimate [µg/m³] (Added as Unused device)

Device ID in the device list is based on the uuid/hostname of the device for easy identification if multiple devices are owned.
Polling Interval is fixed to 10 seconds.
