import json
import os.path, time
import datetime

class nupicConfiguration(object):
    def __init__(self, initialConfiguration, configurationFileLocation, modelFileLocation):
        self._configuration = initialConfiguration
        self._configurationFileLocation = configurationFileLocation
        self._modelFileLocation = modelFileLocation

    def setPredictedField(self, metric):
        self._configuration['inferenceArgs']['predictedField'] = metric;

    def addMetrics(self, metrics):
        for k in range (0, len(metrics)):
            metric = metrics[k];
            self._configuration['includedFields'].append({"fieldName": metric['metric'], "fieldType": metric['metricType'], "maxValue": metric['maxValue'], "minValue": metric['minValue']})
    
    def setDataFileLocation(self, csvFileLocation, uniqueLocation):
        filename = os.path.join(uniqueLocation, csvFileLocation)
        self._configuration['streamDef']['streams'][0]['source'] = "file://" + filename

    def getConfiguration(self):
        return self._configuration

    def modelLastModified(self, uniqueLocation):
        filename = os.path.join(uniqueLocation, self._modelFileLocation)
        if os.path.isfile(self._configurationFileLocation):
            return datetime.datetime.fromtimestamp(os.path.getmtime(self._configurationFileLocation))
        else:
            return datetime.datetime.min
