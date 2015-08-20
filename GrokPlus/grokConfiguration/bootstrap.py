from grokConfiguration.nupicConfiguration import nupicConfiguration
from grokConfiguration.serviceLocator import serviceLocator
from grokConfiguration.couchbaseConfiguration import couchbaseConfiguration
from grokInfrastructure.repository import repository
from grokInfrastructure.csvRepository import csvRepository
from grokInfrastructure.zmqProxy import zmqProxy
from grokInfrastructure.nupicProxy import nupicProxy
from grokTasks.scheduler import scheduler
from grokTasks.modelCreationTask import modelCreationTask
from grokTasks.modelUpdateTask import modelUpdateTask
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
        container['subscriber'] = lambda: zmqProxy(str(subscriberPort), container['repository'](), container['scheduler'](), lambda x: container['modelUpdateTask']().createModelIfOld(x))
        container['nupic'] = lambda: nupicProxy(container['repository']())
        container['nupicConfiguration'] = lambda: nupicConfiguration(configuration['swarmConfiguration'], container['repository'](), configuration['csvFileLocation'])
        container['modelCreationTask'] = lambda: modelCreationTask(container['nupicConfiguration'] (), container['samplesRepository'](), container['metricsRepository'](), container['csvRepository'](), container['nupic']())
        container['modelUpdateTask'] = lambda: modelUpdateTask(container['nupicConfiguration'](), container['modelCreationTask'](), configuration['swarmIntervalInHours'])
        container['espresso'] = lambda: espresso(publisherPort, subscriberPort)
        container['scheduler'] = lambda: myScheduler

        databaseConfiguration.createMapView(configuration['samplesViewName'], configuration['samplesMapFunction'], None)
        databaseConfiguration.createMapView(configuration['metricsViewName'], configuration['metricsMapFunction'], None)

        serviceLocator.setServiceLocator(container)


