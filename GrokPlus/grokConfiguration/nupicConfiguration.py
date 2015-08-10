class nupicConfiguration(object):
    def __init__(self, initialConfiguration):
        self._configuration = initialConfiguration

    def setPredictedField(self, metric):
        self._configuration.inferenceArgs.predictedField = metric;

    def addMetrics(self, metrics, metricType):
        for k in range (0, len(metrics)):
            metric = metrics[k];
            _configuration.includedFields.append({"fieldName": metric.metric, "fieldType": metricType, "maxValue": metric.maxValue, "minValue": metric.minValue})
    
    def getConfiguration(self):
        return self._configuration;


