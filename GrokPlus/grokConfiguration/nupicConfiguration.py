import json
import os.path, time
import datetime

class nupicConfiguration(object):
    def __init__(self, initialConfiguration, repository, csvFileLocation):
        self._configuration = initialConfiguration
        self._repository = repository
        self._csvFileLocation = csvFileLocation

    def setPredictedField(self, metric):
        self._configuration['inferenceArgs']['predictedField'] = metric;

    def addMetrics(self, metrics):
        for k in range (0, len(metrics)):
            metric = metrics[k];
            self._configuration['includedFields'] = {"fieldName": metric['metric'], "fieldType": metric['metricType'], "maxValue": metric['maxValue'], "minValue": metric['minValue']}
    
    def setDataFileLocation(self, uniqueLocation):
        filename = os.path.join(uniqueLocation, self._csvFileLocation)
        self._configuration['streamDef']['streams'][0]['source'] = "file://" + filename

    def getConfiguration(self):
        return self._configuration

    def modelLastModified(self, id):
        model = self._repository.get(id)
        if model != None:
            return datetime.datetime.fromtimestamp(model['timestamp'])
        else:
            return None
