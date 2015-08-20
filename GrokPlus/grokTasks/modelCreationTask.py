import random
import json
import datetime

class modelCreationTask(object):
    def __init__(self, configuration, samplesRepository, metricsRepository, csvRepository, nupic):
        self._configuration = configuration
        self._samplesRepository = samplesRepository
        self._metricsRepository = metricsRepository
        self._nupic = nupic
        self._dataRepository = csvRepository

    def run(self, personId):
        # TODO: have to figure out here how to determine the starttime, endtime and timestep
        # For now maybe defaults like
        # starttime = 7 days ago
        # endtime = now
        # timestep = 15 minutes???
        timestep = 0.06283185307179587
        starttime = 0
        endtime = 94.18494775462199

        metrics = self._metricsRepository.getByView(personId)

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
        self._configuration.setDataFileLocation(personId)

        matrix = self._createSampleMatrix(metrics, personId, startTime, endTime, timeStepInMs)

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

        self._dataRepository.put(matrix, personId)

        self._nupic.permutations_runner(self._configuration, personId)

    def _createSampleMatrix(self, metrics, personId, beginTime, endTime, timeStepInMs):
        matrix = []
        currentMetricCount = 0
        
        for metric in metrics:
            reduceFunction = self._createReduceFunction(metric['reduce'])
            samples = self._samplesRepository.getByView(personId + metric['metric'])

            currentTimeStepCount = 0

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

        


