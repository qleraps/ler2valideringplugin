


import os
import re
import json

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from qgis.PyQt.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QInputDialog
from qgis.PyQt.QtCore import QSettings, QSize
from qgis.core import *
from qgis.gui import QgsMapCanvas, QgsMapToolPan
from datetime import date
from dateutil.relativedelta import relativedelta
# import requests
from .ler2validering_config import API_URLBASE
from .ler2validering_utils import *

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ler2validering_validate.ui'))


class ler2valideringWidgetValidateDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ler2valideringWidgetValidateDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        """
        self.crsComboBox.addItem("WGS84 EPSG:4326", 4326)
        self.crsComboBox.addItem("ETRS89 EPSG:25832", 25832)
        self.crsComboBox.addItem("ETRS89/Kp2000 Jutland EPSG:2196", 2196)
        self.crsComboBox.addItem("ETRS89/Kp2000 Zealand EPSG:2197", 2197)

        self.groupComboBox.addItem("Forsyningstype",1)
        #self.groupComboBox.addItem("Forsyningstype/ledningsjer",2)
        self.groupComboBox.addItem("Ledningsjer/forsyningstype", 3)
        """
        """
        Afløbsledning
        Afløbskomponent
        Vandledning
        Vandkomponent
        Anden ledning
        Anden komponent
        """

        self.objtypeCombo.addItem("Afløbsledning", "afloebsledning")
        self.objtypeCombo.addItem("Afløbsledning", "afloebsledning")
        self.objtypeCombo.addItem("Anden ledning", "andenledning")
        self.objtypeCombo.addItem("Anden komponent", "andenkomponent")
        self.objtypeCombo.addItem("Elledning", "elledning")
        self.objtypeCombo.addItem("Elkomponent", "elkomponent")
        self.objtypeCombo.addItem("Termisk ledning", "termiskledning")
        self.objtypeCombo.addItem("Termisk komponent", "termiskkomponent")
        self.objtypeCombo.addItem("Vandledning", "vandledning")
        self.objtypeCombo.addItem("Vandkomponent", "vandkomponent")


        self.validationconfirmed = False

        # self.tokenEdit.setText(settings.value("lerplus/token"))

        settings = QgsSettings()
        #importcrs = settings.value("lerplusdock/importcrs")
        #importgroup = settings.value("lerplusdock/importgroup")
        # Example: preselect EPSG:4326
        #self.setComboByValue(self.crsComboBox, importcrs)
        #self.setComboByValue(self.groupComboBox, importgroup)

        #sendstyling = settings.value("lerplusdock/importsendstyling")
        #if sendstyling is not None:
        #    self.sendStylingCheckBox.setCheckState(int(sendstyling))

        #manytomulti = settings.value("lerplusdock/importmanytomulti")
        #if manytomulti is not None:
            #self.manyToMultiCheckBox.setCheckState(manytomulti)

        self.okButton.clicked.connect(self.executeValidate)
        self.cancelButton.clicked.connect(self.cancelValidate)

    def setComboByValue(self, combo, value):
        index = combo.findData(value)
        if index != -1:
            combo.setCurrentIndex(index)

    def executeValidate(self):
        self.validationconfirmed = True
        settings = QgsSettings()
        """
        settings.setValue("lerplusdock/importcrs", self.crsComboBox.currentData())
        settings.setValue("lerplusdock/importgroup", self.groupComboBox.currentData())
        settings.setValue("lerplusdock/importsendstyling", self.sendStylingCheckBox.checkState())
        """
        #settings.setValue("lerplusdock/importmanytomulti", self.manyToMultiCheckBox.checkState())
        self.close()

    def setInfo(self, featurecount, objecttype, layer):
        self.featurecount.setText("Antal features: " + str(featurecount))
        if objecttype is False:
            self.objecttype.setText("Objekttype ikke fundet, der skal vælges en type nedenfor")
            self.objtypeCombo.setEnabled(True)
        else:
            self.objecttype.setText("Objekttype: " + objecttype)
            self.objtypeCombo.setEnabled(False)
        self.layername.setText("Layer-navn: " + layer.name())

    def getForcedObjType(self):
        return self.objtypeCombo.currentData()


    def cancelValidate(self):
        self.validationconfirmed = False
        self.close()

    def isConfirmed(self):
        return self.validationconfirmed

    def setIface(self, iface): #, groupname
        self.iface = iface
        #self.groupnameEdit.setText(groupname)

