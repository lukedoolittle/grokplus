from grokConfiguration.nupicConfiguration import nupicConfiguration
from grokConfiguration.serviceLocator import serviceLocator
from grokConfiguration.couchbaseConfiguration import couchbaseConfiguration
from grokAdapters.repository import repository
from grokAdapters.csvRepository import csvRepository
from grokAdapters.zmqAdapter import zmqAdapter
from grokAdapters.nupicAdapter import nupicAdapter
from grokTasks.scheduler import scheduler
from grokTasks.learningTask import learningTask
from grokFramework.jsonPayload import fileToJson
from espresso import espresso

import json

class bootstrap(object):
    def run(self):
        configuration = fileToJson('config.json')
        container = {}

        designDocumentName = configuration['designDocumentName']
        subscriberPort = configuration['subscriberPort']
        publisherPort = configuration['publisherPort']
        couchbaseUrl = configuration['couchbaseUrl']
        samplesViewName = configuration['samplesViewName']
        metricsViewName = configuration['metricsViewName']

        
        myScheduler = scheduler(60) #The scheduler checks every minute for a possible model update
        databaseConfiguration = couchbaseConfiguration(designDocumentName, couchbaseUrl)

        container['repository'] = lambda: repository(couchbaseUrl, designDocumentName, "")
        container['samplesRepository'] = lambda: repository(couchbaseUrl, designDocumentName, samplesViewName)
        container['metricsRepository'] = lambda: repository(couchbaseUrl, designDocumentName, metricsViewName)
        container['csvRepository'] = lambda: csvRepository(configuration['csvFileLocation'])
        container['subscriber'] = lambda: zmqAdapter(str(subscriberPort), container['repository'](), container['scheduler'](), lambda x: container['learningTask']().createModelIfOld(x, configuration['swarmIntervalInHours']))
        container['nupic'] = lambda: nupicAdapter(container['repository']())
        container['nupicConfiguration'] = lambda: nupicConfiguration(configuration['swarmConfiguration'], container['repository'](), configuration['csvFileLocation'])
        container['learningTask'] = lambda: learningTask(container['nupicConfiguration'] (), container['samplesRepository'](), container['metricsRepository'](), container['csvRepository'](), container['nupic']())
        container['espresso'] = lambda: espresso(publisherPort, subscriberPort)
        container['scheduler'] = lambda: myScheduler

        databaseConfiguration.createMapView(configuration['samplesViewName'], configuration['samplesMapFunction'], None)
        databaseConfiguration.createMapView(configuration['metricsViewName'], configuration['metricsMapFunction'], None)

        serviceLocator.setServiceLocator(container)


