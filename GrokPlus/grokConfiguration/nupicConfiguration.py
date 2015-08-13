import json
import os.path, time
import datetime

class nupicConfiguration(object):
    def __init__(self, initialConfiguration, configurationFileLocation):
        self._configuration = initialConfiguration
        self._configurationFileLocation = configurationFileLocation

    def setPredictedField(self, metric):
        self._configuration['inferenceArgs']['predictedField'] = metric;

    def addMetrics(self, metrics):
        for k in range (0, len(metrics)):
            metric = metrics[k];
            self._configuration['includedFields'].append({"fieldName": metric['metric'], "fieldType": metric['metricType'], "maxValue": metric['maxValue'], "minValue": metric['minValue']})
    
    def getConfiguration(self):
        return self._configuration

    def saveConfiguration(self):
        with open(self._configurationFileLocation, 'w') as outfile:
            json.dump(self._configuration, outfile)

    def modelLastModified(self):
        if os.path.isfile(self._configurationFileLocation):
            return time.ctime(os.path.getmtime(self._configurationFileLocation))
        else:
            return datetime.MINYEAR
