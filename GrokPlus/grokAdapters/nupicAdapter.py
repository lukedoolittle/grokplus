import sys
import os
import datetime

import nupic.swarming.permutations_runner

class nupicAdapter(object):
    def __init__(self, repository):
        self._repository = repository

    def permutations_runner(self, swarm_config, id):
      model_params = nupic.swarming.permutations_runner.runWithConfig(swarm_config, {'maxWorkers': 8, 'overwrite':True})
      model_params['timestamp'] = datetime.datetime.now()
      self._repository.putJson(id, model_params)
      print("Finished creating model")
      # TODO do something with this result, with maybe a callback or something
      # model = ModelFactory.create(model_params)




