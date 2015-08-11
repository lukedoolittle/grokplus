from grokConfiguration.nupicConfiguration import nupicConfiguration
from grokConfiguration.serviceLocator import serviceLocator
from grokConfiguration.couchbaseConfiguration import couchbaseConfiguration
from grokAdapters.repository import repository
from grokAdapters.zmqAdapter import zmqAdapter
from grokAdapters.nupicAdapter import nupicAdapter
from grokTasks.scheduler import scheduler
from grokTasks.learningTask import learningTask
from grokFramework.jsonPayload import fileToJson
from grokFramework.jsonPayload import jsonPayload
from espresso import espresso
from couchbase.bucket import Bucket

import json

class bootstrap(object):
    def run(self):
        configuration = fileToJson('config.json')
        container = {}

        designDocumentName = configuration.designDocumentName
        subscriberPort = configuration.subscriberPort
        publisherPort = configuration.publisherPort
        myBucket = Bucket(configuration.couchbaseUrl)

        # 5 second delay after last sample to kick off swarm
        myScheduler = scheduler(5)

        # for testing purposes
        timestep = 0.06283185307179587
        starttime = 0
        endtime = 94.18494775462199

        container['repository'] = lambda: repository(myBucket, designDocumentName)
        container['subscriber'] = lambda: zmqAdapter(str(subscriberPort), container['repository'](), container['scheduler'](), lambda x: container['learningTask']().createModel(x, starttime, endtime, timestep))
        container['nupic'] = lambda: nupicAdapter()
        container['learningTask'] = lambda: learningTask(nupicConfiguration(configuration.swarmConfiguration), container['repository'](), container['nupic'](), configuration.swarmConfigurationFileLocation, configuration.csvFileLocation)
        container['espresso'] = lambda: espresso(publisherPort, subscriberPort)
        container['scheduler'] = lambda: myScheduler

        databaseConfiguration = couchbaseConfiguration(myBucket, designDocumentName)
        databaseConfiguration.createMapView(configuration.samplesViewName, configuration.samplesMapFunction)
        databaseConfiguration.createMapView(configuration.metricsViewName, configuration.metricsMapFunction)

        serviceLocator.setServiceLocator(container)


