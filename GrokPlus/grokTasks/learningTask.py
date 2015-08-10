import csv
import random

class learningTask(object):
    def __init__(self, configuration, repository, nupic, configurationFileLocation, csvFileLocation):
        self._configuration = configuration
        self._repository = repository
        self._nupic = nupic
        self._configurationFileLocation = configurationFileLocation
        self._csvFileLocation = csvFileLocation

    def createModel(self, personId):
        pass
        # have to figure out here how to determine the starttime, endtime and timestep

    def createModel(self, personId, starttime, endtime, timestep):
        metrics = repository.getByView("metricsView", personId)

        #for now we'll randomly pick a metric
        targetMetric = random.choice(metrics)
        
        return self.swarm(personId, metrics, targetMetric.metric, starttime, endtime, timestep)

    def swarm(self, personId, metrics, targetMetric, startTime, endTime, timeStepInMs):
        self._configuration.addMetrics(metrics)
        self._configuration.setPredictedField(self, targetMetric)
        with open(self._configurationFileLocation, 'w') as outfile:
            outfile.write(self._configuration.getConfiguration())

        matrix = self._createSampleMatrix(metrics, "sampleView", personId)

        flags = ["" for metric in metrics]
        dataTypes.insert(0, "")
        matrix.insert(0, flags)

        metricNames = [metric.metric for metric in metrics]
        metricNames.insert(0, "timestamp")
        matrix.insert(0, dataTypes)

        dataTypes = [metric.metricType for metric in metrics]
        dataTypes.insert(0, "float")  # marking the timestamp column as a float
        matrix.insert(0, metricNames)

        with open(self._csvFileLocation, "wb") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(matrix)

        #change this here so we don't have to write to a file
        #TODO uncomment this
        #self._nupic.permutations_runner(self._configurationFileLocation)

    def forecast(self):
        pass

    def anomoly(self):
        pass

    def _createSampleMatrix(self, metrics, sampleViewName, personId, beginTime, endTime, timeStepInMs):
        matrix = []
        currentMetricCount = 0
        
        for metric in metrics:
            reduceFunction = self._createReduceFunction(metric.reduce)
            samples = self._repository.getByView("samplesView", personId + metric.metric)

            currentTimeStepCount = 0
            while True:
                currentTimeStepStart = beginTime + (timeStepInMs * currentTimeStepCount)
                currentTimeStepEnd = beginTime + (timeStepInMs * (currentTimeStepCount + 1))
                my_list = [sample for sample in samples if sample.timestamp >= currentTimeStepStart and sample.timestamp < currentTimeStepEnd]

                if len(my_list) == 0:
                    value = None
                else:
                    value = reduceFunction(my_list)

                if len(matrix) == currentTimeStepCount:
                    matrix.append([currentTimeStepStart])

                matrix[currentTimeStepCount].append(value)
                currentTimeStepCount += 1
                if currentTimeStepEnd >= endTime:
                    break
            currentMetricCount += 1
        return matrix

    def _createReduceFunction(self, reduceType):
        if reduceType == 'Sum':
            return lambda x: sum(float(i.value) for i in x)
        else:
            return lambda x: sum(float(i.value) for i in x)/len(x)

        


