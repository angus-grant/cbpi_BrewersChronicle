from modules import cbpi
import requests
import time

#version 1.3.0.0

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

  for i, fermenter in cbpi.cache.get("fermenter").iteritems():
    if fermenter.state is not False:
        try:
            writeReadingsToBC = True
            logBC(" ")

            try:
                fermentInfo_uri = bc_base_uri + "fermentLogs/GetFermentLogInfoByAssetName"
                data = {"AssetAPIId": fermenter.name, "ReadingValue": "", "ControlSoftwareName": "CraftBeerPi"}
                headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + api_key}
                response = requests.post(fermentInfo_uri, json=data, headers = headers, timeout = 1)
                responseData = response.json()
            except Exception as e:
                logBC("exception getting info from BC: {0}".format(e))

            if response.status_code == 400:
                cbpi.notify("BC", response.content, type="danger", timeout=30000)
                logBC("attempting to stop fermenter")
                fermenter.instance.stop()
                fermenter.state = not fermenter.state

                brewName = ""
                targetTemperature = 0

                writeReadingsToBC = False
            else:
                logBC("trying to get responseData")
                brewName = responseData['Name']
                targetTemperature = responseData['TargetTemperature']

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
                    targetTemperature = 0
                targetTemp_api_url = "http://localhost:5000/api/fermenter/{0}/targettemp/{1}".format(fermenter.id, targetTemperature)
                headers = {'content-type': 'application/json'}
                requests.post(targetTemp_api_url, data="", headers = headers, timeout = 1)
            except Exception as e:
                logBC("exception writing target temp to CBPi from BC info: {0}".format(e))
                pass

            if bool(writeReadingsToBC) is True:
                logBC("writing readings to BC")

                try:
                    bc_post_reading = bc_base_uri + "fermentLogs/PostReadingByAPIId"
                    temp = fermenter.instance.get_temp()
                    sensorName = cbpi.cache['sensors'][int(fermenter.sensor)].name
                    data = {"AssetAPIId": sensorName, "ReadingValue": temp, "ControlSoftwareName": "CraftBeerPi"}
                    headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + api_key}
                    response = requests.post(bc_post_reading, json=data, headers = headers, timeout = 1)
                    
                    if response.status_code == 400:
                        cbpi.notify("BC", response.content, type="danger", timeout=30000)
                        logBC("attempting to stop fermentor")
                        fermenter.instance.stop()
                        fermenter.state = not fermenter.state

                        brewName = ""
                        targetTemperature = 0

                        writeReadingsToBC = False
                    else:
                        sensorName = fermenter.name + " target temp"
                        data = {"AssetAPIId": sensorName, "ReadingValue": targetTemperature, "ControlSoftwareName": "CraftBeerPi" }
                        headers = {'content-type': 'application/json', 'Authorization': 'Bearer ' + api_key }
                        response = requests.post(bc_post_reading, json=data, headers = headers, timeout = 1)

                        cbpi.notify("Brewers Chronicle", "Readings for fermentor {0} submitted to Brewers Chronicle".format(fermenter.name), timeout=15000)

                        logBC("readings written successfully to BC")

                except Exception as e:
                    logBC("exception writing target temp to BrewersChronicle: {0}".format(e))
                    pass
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
        self.notify("Actor Error", "Failed to setup actor %s. Please check the configuraiton" % value.name, type="danger", timeout=None)
        self.app.logger.error("Initializing of Actor %s failed" % id)
