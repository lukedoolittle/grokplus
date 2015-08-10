from grokConfiguration.couchbaseConfiguration import couchbaseConfiguration
from grokConfiguration.nupicConfiguration import nupicConfiguration
from grokProxies.zmqProxy import zmqProxy
from couchbase.bucket import Bucket
from grokProxies.repository import repository
from grokProxies.nupicAdapter import nupicAdapter
from grokTasks.learningTask import learningTask
from grokConfiguration.serviceLocator import serviceLocator
from espresso import espresso
import json

import json

class jsonPayload(object):
    def __init__(self, filename):
        with open(filename) as data_file:    
            configuration = json.load(data_file)
        self.__dict__ = json.loads(data)

class bootstrap(object):
    def run(self):
        configuration = jsonPayload('config.json')
        container = {}

        designDocumentName = configuration.designDocumentName
        subscriberPort = configuration.subscriberPort
        publisherPort = configuration.publisherPort

        myBucket = Bucket(configuration.couchbaseUrl)

        container['repository'] = lambda: repository(myBucket, designDocumentName)
        container['subscriber'] = lambda: zmqProxy(str(subscriberPort), container['repository']())
        container['nupic'] = lambda: nupicAdapter()
        container['learningTask'] = lambda: learningTask(nupicConfiguration(configuration.swarmConfiguration), container['repository'](), container['nupic'](), configuration.swarmConfigurationFileLocation, configuration.csvFileLocation)
        container['espresso'] = lambda: espresso(publisherPort, subscriberPort)

        databaseConfiguration = couchbaseConfiguration(myBucket, designDocumentName)
        databaseConfiguration.createMapView(configuration.samplesViewName, configuration.samplesMapFunction)
        databaseConfiguration.createMapView(configuration.metricsViewName, configuration.metricsMapFunction)

        serviceLocator.setServiceLocator(container)


