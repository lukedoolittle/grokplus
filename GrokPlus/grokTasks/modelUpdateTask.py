import datetime

class modelUpdateTask(object):
    def __init__(self, configuration, task, swarmIntervalInHours):
        self._configuration = configuration
        self._task = task
        self._swarmIntervalInHours = swarmIntervalInHours

    def createModelIfOld(self, personId):
        modelLastModified = self._configuration.modelLastModified(personId)
        if modelLastModified != None:
            modelAgeInHours = (datetime.datetime.now() - modelLastModified).seconds//3600
        if modelLastModified == None or modelAgeInHours > self._swarmIntervalInHours:
            self._task.run(personId)


