from grokConfiguration.nupicConfiguration import nupicConfiguration
from grokConfiguration.serviceLocator import serviceLocator
from grokConfiguration.couchbaseConfiguration import couchbaseConfiguration
from grokAdapters.repository import repository
from grokAdapters.zmqAdapter import zmqAdapter
from grokAdapters.nupicAdapter import nupicAdapter
from grokTasks.scheduler import scheduler
from grokTasks.learningTask import learningTask
from espresso import espresso
from couchbase.bucket import Bucket

import json

class jsonPayloadFromFile(object):
    def __init__(self, filename):
        with open(filename, "r") as data_file:    
            data = data_file.read().replace('\n', '').replace("\xEF", "").replace("\xBB", "").replace("\xBF", "")
        self.__dict__ = json.loads(data)

class bootstrap(object):
    def run(self):
        configuration = jsonPayloadFromFile('config.json')
        container = {}

        designDocumentName = configuration.designDocumentName
        subscriberPort = configuration.subscriberPort
        publisherPort = configuration.publisherPort

        myBucket = Bucket(configuration.couchbaseUrl)

        myScheduler = scheduler()

        #for testing purposes
        timestep = 0.06283185307179587
        starttime = 0
        endtime = 94.18494775462199

        container['repository'] = lambda: repository(myBucket, designDocumentName)
        container['subscriber'] = lambda: zmqAdapter(str(subscriberPort), container['repository'](), container['scheduler'](), lambda x: container['nupic']().createModel(x, starttime, endtime, timestep))
        #container['nupic'] = lambda: nupicAdapter()
        container['learningTask'] = lambda: learningTask(nupicConfiguration(configuration.swarmConfiguration), container['repository'](), container['nupic'](), configuration.swarmConfigurationFileLocation, configuration.csvFileLocation)
        container['espresso'] = lambda: espresso(publisherPort, subscriberPort)
        container['scheduler'] = lambda: myScheduler

        databaseConfiguration = couchbaseConfiguration(myBucket, designDocumentName)
        databaseConfiguration.createMapView(configuration.samplesViewName, configuration.samplesMapFunction)
        databaseConfiguration.createMapView(configuration.metricsViewName, configuration.metricsMapFunction)

        serviceLocator.setServiceLocator(container)


