from modules import cbpi
from modules.core.hardware import SensorActive
from modules.core.props import Property
from flask import Blueprint, render_template, jsonify, request

import requests
import time

blueprint = Blueprint('bc_gravity', __name__)

#version 1.3.0.0

# bc_base_uri = "http://192.168.0.27:51402/api/"
bc_base_uri = "http://api.brewerschronicle.com/api/"

def bc_api_key():
  api_key = cbpi.get_config_parameter('brewerschronicle_api_key', None)
  if api_key is None:
    cbpi.add_config_parameter("brewerschronicle_api_key", "", "text", "Brewers Chronicle API Key")
    return ""
  else:
    return api_key

@cbpi.backgroundtask(key="brewerschronicle_task", interval=900)
def brewerschronicle_background_task(api):
  api_key = bc_api_key()
  if api_key == "":
    return

  for i, fermenter in cbpi.cache.get("fermenter").items():
    if fermenter.state is not False:
        try:
            writeReadingsToBC = True
            logBC(" ")

            try:
                fermentInfo_uri = bc_base_uri + "fermentLogs/GetFermentLogInfoByAssetName"
                data = {"AssetName": fermenter.name, "AssetAPIId": fermenter.name, "ReadingValue": "", "ControlSoftwareName": "CraftBeerPi"}
                headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + api_key}
                response = requests.post(fermentInfo_uri, json=data, headers = headers, timeout = 1)
                responseData = response.json()

                logBC("response.status_code: {0}".format(response.status_code))

                if response.status_code == 400 or response.status_code == 500:
                    brewName = ""
                    targetTemperature = -50.0
                    currentGravity = "-"
                else:
                    logBC("trying to get responseData")
                    brewName = responseData['Name']
                    targetTemperature = responseData['TargetTemperature']

                    currentGravity = responseData['LatestGravity']
                    if currentGravity == None:
                        currentGravity = "-"

                try:
                    set_name_uri = "http://localhost:5000/api/fermenter/{0}/brewname".format(fermenter.id)
                    headers = {'content-type': 'application/json'}
                    data = {"brewname": brewName}
                    requests.post(set_name_uri, json=data, headers = headers, timeout = 1)
                except Exception as e:
                    logBC("exception writing brew name: {0}".format(e))
                    pass

                try:
                    if targetTemperature == -50.0:
                        targetTemperature = fermenter.instance.get_target_temp()

                    if targetTemperature != -50.0:
                        targetTemp_api_url = "http://localhost:5000/api/fermenter/{0}/targettemp/{1}".format(fermenter.id, targetTemperature)
                        headers = {'content-type': 'application/json'}
                        requests.post(targetTemp_api_url, data="", headers = headers, timeout = 1)
                except Exception as e:
                    logBC("exception writing target temp to CBPi from BC info: {0}".format(e))
                    pass

                cbpi.cache['sensors'][int(fermenter.sensor3)].instance.gravity = currentGravity

                if bool(writeReadingsToBC) is True:
                    logBC("writing readings to BC")

                    try:
                        bc_post_reading = bc_base_uri + "fermentLogs/PostReadingByAPIId"
                        temp = fermenter.instance.get_temp()
                        sensorName = cbpi.cache['sensors'][int(fermenter.sensor)].name
                        data = {"AssetName": fermenter.name, "AssetAPIId": sensorName, "ReadingValue": temp, "ControlSoftwareName": "CraftBeerPi"}
                        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + api_key}
                        response = requests.post(bc_post_reading, json=data, headers = headers, timeout = 1)
                        
                        if response.status_code == 400:
                            cbpi.notify("BC", response.content, type="danger", timeout=30000)

                        if targetTemperature != -50.0:
                            logBC("logging target temp")
                            sensorName = fermenter.name + " target temp"
                            data = {"AssetName": fermenter.name, "AssetAPIId": sensorName, "ReadingValue": targetTemperature, "ControlSoftwareName": "CraftBeerPi" }
                            headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + api_key }
                            response = requests.post(bc_post_reading, json=data, headers = headers, timeout = 1)

                        cbpi.notify("Brewers Chronicle", "Readings for fermentor {0} submitted to Brewers Chronicle".format(fermenter.name), timeout=15000)

                        logBC("readings written successfully to BC")

                    except Exception as e:
                        logBC("exception writing target temp to BrewersChronicle: {0}".format(e))
                        pass
            except Exception as e:
                logBC("exception getting info from BC: {0}".format(e))

        except Exception as e:
            logBC("Exception: {0}".format(e))
            pass

def logBC(text):
    try:
        filename = "./logs/BrewersChronicle.log"
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        with open(filename, "a") as file:
            file.write("%s,%s\n" % (formatted_time, text))

    except Exception as e:
        cbpi.emit(e, "")
        self.notify("Actor Error", "Failed to setup actor %s. Please check the configuration" % value.name, type="danger", timeout=None)
        self.app.logger.error("Initializing of Actor %s failed" % id)

@cbpi.sensor
class BC_GravitySensor(SensorActive):

    gravity = Property.Number("Gravity", configurable=False, default_value=1050, description="Latest Gravity reading from Brewers Chronicle")

    def get_unit(self):
        '''
        :return: Unit of the sensor as string. Should not be longer than 3 characters
        '''
        return ""

    def stop(self):
        SensorPassive.stop(self)

    def execute(self):
        '''
        Active sensor has to handle his own loop
        :return: 
        '''
        while self.is_running() is True:
            self.data_received(self.gravity)
            self.sleep(5)

    @classmethod
    def init_global(cls):
        '''
        Called one at the startup for all sensors
        :return: 
        '''
        cbpi.app.register_blueprint(blueprint)
