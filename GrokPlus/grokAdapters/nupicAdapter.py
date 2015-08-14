import sys
import os

import nupic.swarming.permutations_runner

class nupicAdapter(object):
    def __init__(self):
        pass

    def permutations_runner(self, swarm_config):
      model_params = permutations_runner.runWithConfig(swarm_config, {'maxWorkers': 8})
      # TODO do something with this result, with maybe a callback or something
      model = ModelFactory.create(model_params)




