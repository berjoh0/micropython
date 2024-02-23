import ConnectWiFi
import Http
import json
import machine, onewire, ds18x20, time

print("Connecting")

ssid = "XXXXX"
password = "YYYYY"

ConnectWiFi.connect(ssid, password)


test_pin = machine.Pin(1, machine.Pin.IN)

ds_pin = machine.Pin(4)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

roms = ds_sensor.scan()
print('Found DS devices: ', roms)


while True:
    retServerTime = Http.http_get('http://192.168.3.89/time');
    retJson = json.loads(Http.body)
    print(retJson["timestampmillis"])

    ds_sensor.convert_temp()

    jsonData = {
        "sensor": [{
            "siteID": "10002",
            "sensorID": "20036",
            "timestamp" : retJson["timestampmillis"],
            "value": ds_sensor.read_temp(roms[0])
        }]
    }

    print(jsonData)

    retData = Http.http_post('http://192.168.3.89/sensor/Sensor', jsonData);

    print(retData)

    time.sleep(900)



