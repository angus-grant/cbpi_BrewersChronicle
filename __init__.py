from modules import cbpi
import requests
import time

bc_uri = "https://api.brewerschronicle.com/api/readings/cbpi"

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
        components = fermenter.brewname.split("|");
        brew_name = components[0]

        logBC("Starting temperature post for {0}".format(brew_name))

        ferment_id = components[1]
        temp = fermenter.instance.get_temp()
        unit = cbpi.get_config_parameter("unit", "C")
        data = {"api_key": api_key, "ferment_id": ferment_id, "temperature": temp, "temp_unit": unit}
        logBC("Temperature post payload: {0}".format(data))

        response = requests.post(bc_uri, json=data)
        data = response.json()
        set_temp = data['set_temp']
        logBC("set_temp: {0}".format(set_temp))

        temp_api_url = "http://localhost:5000/api/fermenter/{0}/targettemp/{1}".format(fermenter.id, set_temp)
        headers = {'content-type': 'application/json'}
        logBC(temp_api_url)
        requests.post(temp_api_url, data="", headers = headers, timeout = 1)
        logBC(response)

        logBC(fermenter.instance.get_target_temp())
        logBC(fermenter.instance.cache_key)

        message = "{0}: Temp posted".format(brew_name)
        cbpi.notify("Brewers Chronicle", message, type="info", timeout=None)
        logBC(message)

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


