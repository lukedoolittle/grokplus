from grokConfiguration.nupicConfiguration import nupicConfiguration
from grokConfiguration.serviceLocator import serviceLocator
from grokConfiguration.couchbaseConfiguration import couchbaseConfiguration
from grokAdapters.repository import repository
from grokAdapters.zmqAdapter import zmqAdapter
from grokAdapters.nupicAdapter import nupicAdapter
from grokTasks.scheduler import scheduler
from grokTasks.learningTask import learningTask
from grokFramework.jsonPayload import fileToJson
from espresso import espresso
from couchbase.bucket import Bucket

import json

class bootstrap(object):
    def run(self):
        configuration = fileToJson('config.json')
        container = {}

        designDocumentName = configuration['designDocumentName']
        subscriberPort = configuration['subscriberPort']
        publisherPort = configuration['publisherPort']
        couchbaseUrl = configuration['couchbaseUrl']
        myBucket = Bucket(couchbaseUrl)

        # scheduler will run jobs every 10 seconds
        myScheduler = scheduler(10)

        # for testing purposes
        timestep = 0.06283185307179587
        starttime = 0
        endtime = 94.18494775462199

        container['repository'] = lambda: repository(lambda: Bucket(couchbaseUrl), designDocumentName)
        container['subscriber'] = lambda: zmqAdapter(str(subscriberPort), container['repository'](), container['scheduler'](), lambda x: container['learningTask']().createModelIfOld(x, starttime, endtime, timestep))
        container['nupic'] = lambda: nupicAdapter()
        container['nupicConfiguration'] = lambda: nupicConfiguration(configuration['swarmConfiguration'], configuration['swarmConfigurationFileLocation'], configuration['swarmModelFileLocation'])
        container['learningTask'] = lambda: learningTask(container['nupicConfiguration'] (), container['repository'](), container['nupic'](), configuration['csvFileLocation'], configuration['swarmIntervalInHours'])
        container['espresso'] = lambda: espresso(publisherPort, subscriberPort)
        container['scheduler'] = lambda: myScheduler

        databaseConfiguration = couchbaseConfiguration(myBucket, designDocumentName)
        databaseConfiguration.createMapView(configuration['samplesViewName'], configuration['samplesMapFunction'], None)
        databaseConfiguration.createMapView(configuration['metricsViewName'], configuration['metricsMapFunction'], None)
        databaseConfiguration.createMapView(configuration['sampleCountViewName'], configuration['sampleCountMapFunction'], configuration['sampleCountReduceFunction'])

        # TODO need to prime the scheduler if there are any existing samples / models

        serviceLocator.setServiceLocator(container)


