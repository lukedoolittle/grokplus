import csv

class jsonPayload(object):
    def __init__(self, object):
        self.__dict__ = object

class learningTask(object):
    def __init__(self, configuration, repository, nupic, configurationFileLocation, csvFileLocation):
        self._configuration = configuration
        self._repository = repository
        self._nupic = nupic
        self._configurationFileLocation = configurationFileLocation
        self._csvFileLocation = csvFileLocation

    def swarm(self, personId, targetMetric, startTime, endTime, timeStepInMs):
        metrics = repository.getByView("metricsView", personId)
        self._configuration.addMetrics(metrics, "float")
        self._configuration.setPredictedField(self, targetMetric)
        with open(self._configurationFileLocation, 'w') as outfile:
            outfile.write(self._configuration.getConfiguration())

        matrix = self._createSampleMatrix(metrics, "sampleView", personId)

        metricNames = [metric["metric"] for metric in metrics]
        metricNames.insert(0, "timestamp")
        dataTypes = ["float" for metric in metricNames]
        flags = ["" for metric in metricNames]

        matrix.insert(0, flags)
        matrix.insert(0, dataTypes)
        matrix.insert(0, metricNames)

        with open(self._csvFileLocation, "wb") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(matrix)

        self._nupic.permutations_runner(self._configurationFileLocation)

    def forecast(self):
        pass

    def anomoly(self):
        pass

    def _createSampleMatrix(self, metrics, sampleViewName, personId, beginTime, endTime, timeStepInMs):
        matrix = []
        currentMetricCount = 0
        
        for metricDictionary in metrics:
            metric = jsonPayload(metricDictionary)
            reduceFunction = self._createReduceFunction(metric.reduce)
            print("getting all samples for metric " + metric.metric)
            samples = self._repository.getByView("samplesView", personId + metric.metric)

            currentTimeStepCount = 0
            print("starting creation loop....")
            while True:
                currentTimeStepStart = beginTime + (timeStepInMs * currentTimeStepCount)
                currentTimeStepEnd = beginTime + (timeStepInMs * (currentTimeStepCount + 1))
                my_list = [sample for sample in samples if sample['timestamp'] >= currentTimeStepStart and sample['timestamp'] < currentTimeStepEnd]

                if len(my_list) == 0:
                    value = None
                else:
                    value = reduceFunction(my_list)

                if len(matrix) == currentTimeStepCount:
                    matrix.append([currentTimeStepStart])

                matrix[currentTimeStepCount].append(value)
                print("finished creating value for time step " + str(currentTimeStepCount))
                currentTimeStepCount += 1
                if currentTimeStepEnd >= endTime:
                    break
            currentMetricCount += 1
        return matrix

    def _createReduceFunction(self, reduceType):
        if reduceType == 'sum':
            return lambda x: sum(float(i['value']) for i in x)
        else:
            return lambda x: sum(float(i['value']) for i in x)/len(x)

        


