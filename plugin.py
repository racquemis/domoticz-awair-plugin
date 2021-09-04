# Awair Element Air Quality Plugin
#
# Author: Racquemis
#
"""
<plugin key="AwairLocalPlugin" name="Awair Element Air Quality" author="racquemis" version="1.0.0" wikilink="https://github.com/racquemis/domoticz-awair-plugin" externallink="https://github.com/racquemis/domoticz-awair-plugin">
    <description>
        <h2>Awair Element Plugin (Local API)</h2>
        Plugin for Awair Element Air Quality data
        <h3>Instructions</h3><br/>
        Local API has to be enabled in the Awair Home app:<br/>
        1. Tap Awair+ tab in the lower right-hand corner of the Awair Home App<br/>
        2. Tap "Awair APIs Beta" in the Awair+ menu<br/>
        3. Tap "Local API" in the Awair APIs menu<br/>
        4. Tap "Enable Local API" to enable the feature for your Awair device<br/>
        <br/><br/>
        Fill in the device IP Address in the field below.
        The ip address can be retrieved on the DHCP server on your router.<br/>
        It is recommended to make a DHCP reservation for the device.
    </description>
    <params>
        <param field="Address" label="IP Address" width="200px" required="true" default="0.0.0.0"/>
    </params>
</plugin>
"""
import Domoticz
import requests
import json

class BasePlugin:
    #enabled = False
    def __init__(self):
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        Domoticz.Heartbeat(10)
        try:
            headers = {'content-type':'application/json'}
            host = Parameters["Address"] if len(Parameters["Address"].split('.')) == 4 else Parameters["Address"] + ".local"
            response_awair = requests.get("http://"+host+"/settings/config/data", headers=headers, timeout=(10,10))
            json_items = json.loads(response_awair.text)
            awair_uuid = json_items["device_uuid"].split("_")[-1]
            response_awair.close()
            if len(Devices) == 0:
                    Domoticz.Device(DeviceID=awair_uuid, Name="[Score]", Unit=1, Used=1, Type=243, Subtype=6).Create()
                    Domoticz.Device(DeviceID=awair_uuid, Name="[Temp/Hum]", Unit=2, Used=1, Type=82).Create()
                    Domoticz.Device(DeviceID=awair_uuid, Name="[CO2]", Unit=3, Used=1, Type=249).Create()
                    Domoticz.Device(DeviceID=awair_uuid, Name="[VOC]", Unit=4, Used=1, Type=243, Subtype=31, Options={'Custom': '1;ppb'}).Create()
                    Domoticz.Device(DeviceID=awair_uuid, Name="[PM2.5]", Unit=5, Used=1, Type=243, Subtype=31, Options={'Custom': '1;µg/m³'}).Create()
                    Domoticz.Device(DeviceID=awair_uuid, Name="[PM10*]", Unit=6, Used=0, Type=243, Subtype=31, Options={'Custom': '1;µg/m³'}).Create()
        except requests.exceptions.Timeout as e:
            Domoticz.Error(str(e))
        except ValueError as e:
            Domoticz.Error(str(e))
    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        Domoticz.Log("onHeartbeat called")
        headers = {'content-type':'application/json'}
        try:
            host = Parameters["Address"] if len(Parameters["Address"].split('.')) == 4 else Parameters["Address"] + ".local"
            awair_request = requests.get("http://"+host+"/air-data/latest", headers=headers, timeout=(10,10))
            Domoticz.Debug("http://"+host+"/air-data/latest")
            json_items = json.loads(awair_request.text)
            awair_request.close()
            if "score" in json_items:
                Devices[1].Update(nValue=0,sValue=str(json_items["score"]))
            if "temp" in json_items and "humid" in json_items:
                Devices[2].Update(nValue=0,sValue=str(json_items["temp"])+";"+str(json_items["humid"]))
            if "co2" in json_items:
                Devices[3].Update(nValue=json_items["co2"], sValue="")
            if "voc" in json_items:
                Devices[4].Update(nValue=0,sValue=str(json_items["voc"]))
            if "pm25" in json_items:
                Devices[5].Update(nValue=0,sValue=str(json_items["pm25"]))
            if "pm10_est" in json_items:
                Devices[6].Update(nValue=0,sValue=str(json_items["pm10_est"]))  
        except requests.exceptions.Timeout as e:
            Domoticz.Error(str(e))
        except ValueError as e:
            Domoticz.Error(str(e))   
            

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()
    

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
