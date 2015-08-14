import csv
import random
import json
import datetime

class learningTask(object):
    def __init__(self, configuration, repository, nupic, csvFileLocation, swarmIntervalInHours):
        self._configuration = configuration
        self._repository = repository
        self._nupic = nupic
        self._csvFileLocation = csvFileLocation
        self._swarmIntervalInHours = swarmIntervalInHours

    def createModelIfOld(self, personId, starttime, endtime, timestep):
        modelAgeInHours = (datetime.datetime.now() - self._configuration.modelLastModified(personId)).seconds//3600
        if modelAgeInHours > self._swarmIntervalInHours:
            self.createModel(personId, starttime, endtime, timestep)

    def createModel(self, personId):
        pass
        # TODO: have to figure out here how to determine the starttime, endtime and timestep

    def createModel(self, personId, starttime, endtime, timestep):
        metrics = self._repository.getByView("metricsView", personId)

        # remove any duplicate metric definitions; for now the pruning is arbitrary
        seen = set()
        seen_add = seen.add
        uniqueMetrics = [ x for x in metrics if not (x['personId']+x['metric'] in seen or seen_add(x['personId']+x['metric'])) ]

        # for now we'll randomly pick a metric
        targetMetric = random.choice(uniqueMetrics)
        
        return self.swarm(personId, uniqueMetrics, targetMetric['metric'], starttime, endtime, timestep)

    def swarm(self, personId, metrics, targetMetric, startTime, endTime, timeStepInMs):
        self._configuration.addMetrics(metrics)
        self._configuration.setPredictedField(targetMetric)
        #self._configuration.saveConfiguration(personId)

        matrix = self._createSampleMatrix(metrics, "sampleView", personId, startTime, endTime, timeStepInMs)

        #TODO (structural) you can simplify this with syntax
        flags = ["" for metric in metrics]
        flags.insert(0, "")
        matrix.insert(0, flags)

        dataTypes = [metric['metricType'] for metric in metrics]
        dataTypes.insert(0, "float")  # marking the timestamp column as a float
        matrix.insert(0, dataTypes)

        metricNames = [metric['metric'] for metric in metrics]
        metricNames.insert(0, "timestamp")
        matrix.insert(0, metricNames)

        #TODO (structural) use the repository for this
        with open(self._csvFileLocation, "wb") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(matrix)

        #self._nupic.permutations_runner(self._configurationFileLocation)
        self._nupic.permutations_runner(self._configuration.getConfiguration())

    def forecast(self):
        pass

    def anomoly(self):
        pass

    def _createSampleMatrix(self, metrics, sampleViewName, personId, beginTime, endTime, timeStepInMs):
        matrix = []
        currentMetricCount = 0
        
        for metric in metrics:
            reduceFunction = self._createReduceFunction(metric['reduce'])
            print("call to database to get all samples for " + personId + metric['metric'])
            samples = self._repository.getByView("samplesView", personId + metric['metric'])
            currentTimeStepCount = 0
            print("got samples counting size")
            samplecount = 0
            for sample in samples:
                samplecount += 1
            print("retrieved " + str(samplecount) + " samples")
            while True:
                currentTimeStepStart = beginTime + (timeStepInMs * currentTimeStepCount)
                currentTimeStepEnd = beginTime + (timeStepInMs * (currentTimeStepCount + 1))
                my_list = [sample for sample in samples if float(sample['timestamp']) >= currentTimeStepStart and float(sample['timestamp']) < currentTimeStepEnd]

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
            return lambda x: sum(float(i['value']) for i in x)
        else:
            return lambda x: sum(float(i['value']) for i in x)/len(x)

        


