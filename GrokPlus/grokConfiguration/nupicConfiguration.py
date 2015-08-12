class nupicConfiguration(object):
    def __init__(self, initialConfiguration):
        self._configuration = initialConfiguration

    def setPredictedField(self, metric):
        self._configuration['inferenceArgs']['predictedField'] = metric;

    def addMetrics(self, metrics):
        for k in range (0, len(metrics)):
            metric = metrics[k];
            self._configuration['includedFields'].append({"fieldName": metric['metric'], "fieldType": metric['metricType'], "maxValue": metric['maxValue'], "minValue": metric['minValue']})
    
    def getConfiguration(self):
        return self._configuration


