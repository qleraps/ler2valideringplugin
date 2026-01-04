from .ler2validering_config import *
from qgis.core import *
from qgis.PyQt.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QInputDialog
import json
import requests
import time


def is_valid_json(my_string):
    try:
        json.loads(my_string)
        return True
    except json.JSONDecodeError:
        return False


def inDebugMode():
    #return False
    settings = QgsSettings()
    if settings.value("ler2validering/debugmode") == "1":
        return True
    else:
        return False

def make_api_call(self, apifunction, data='', timeout=60):
    settings = QgsSettings()
    token = settings.value("lerplusdock/apitoken")
    # QMessageBox.information(self, 'Token', token)
    API_ENDPOINT = API_URLBASE + '/' + apifunction + '?apitoken=' + token +'&apiversion=' + API_VERSION + "&pluginversion=" + PLUGIN_VERSION
    if inDebugMode():
        if data != '':
            jsdata = json.dumps(data, sort_keys=True, indent=4)
            QMessageBox.information(self, 'Sending to API', API_ENDPOINT + '\n' + jsdata)
        else:
            QMessageBox.information(self, 'Sending to API', API_ENDPOINT)
    try:
        start = time.time()
        r = requests.post(url=API_ENDPOINT, data=data, timeout=timeout)
        end=time.time()
        print ("postrequest elapsed = "+ str(end - start) + "seconds")
        #print(r.raise_for_status())
        #r.raise_for_status()
    except requests.exceptions.Timeout:
        QMessageBox.information(self, 'The request timed out','')
        print("The request timed out")
        return False
    except requests.exceptions.RequestException as e:
        QMessageBox.information(self, f"An error occurred: ", e)
        print(f"An error occurred: {e}")
        return False
    #r = requests.post(url=API_ENDPOINT, data=data)

    if not is_valid_json(r.text):
        QMessageBox.information(self, 'Invalid API-response', r.text)
        return False
    data = json.loads(r.text)
    #QMessageBox.information(self, 'ERROR! API-response', r.text)
    if data["status"] != 'ok':
        if inDebugMode():
            QMessageBox.information(self, 'ERROR! API-response', r.text)
        else:
            error = data["data"]["errortext"]
            QMessageBox.information(self, 'LER2-validering backend returnerede en fejl', error)
            #QMessageBox.information(self, 'Fejl', "Der skete en fejl ved kald af " + apifunction + ": \n" + error)
        return False
    if inDebugMode():
        QMessageBox.information(self, 'API-response', r.text)

    return data
