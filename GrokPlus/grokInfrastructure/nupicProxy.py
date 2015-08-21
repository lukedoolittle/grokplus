import sys
import os
import datetime

import nupic.swarming.permutations_runner

class nupicProxy(object):
    def __init__(self, repository):
        self._repository = repository

    def permutations_runner(self, configuration, id):
      
      swarm_config = configuration.getConfiguration()
      outputDirectory = configuration.getOutputLocation(id)
      model_params = nupic.swarming.permutations_runner.runWithConfig(swarm_config, {'maxWorkers': 8, 'overwrite':True}, outDir=outputDirectory, permWorkDir=outputDirectory)
      model_params['timestamp'] = datetime.datetime.now()
      self._repository.putJson(json=model_params, id=id)
      #global gCurrentSearch
      #gCurrentSearch.peekSearchJob().getJobStatus(gCurrentSearch._workers).getResults()["fieldContributions"]
      # OR
      #the .pk1 file that is created should have this information (pickle file???)
      # TODO do something with this result, with maybe a callback or something

    def create_model(self):
        model_params = self._repository.get(personId)
        model = ModelFactory.create(model_params)




