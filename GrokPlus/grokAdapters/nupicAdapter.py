import sys
import os

import nupic.swarming.permutations_runner

class nupicAdapter(object):
    def __init__(self):
        pass

    def permutations_runner(self, swarm_config):
      #f = open('result.txt', 'w')
      # TODO (structural) use runWithConfig to dodge having to write the json configuration to a file
      #permutations_runner.runWithJsonFile(fileArgPath, optionsDict, outputLabel, permWorkDir) >> 'Filename:', filename
      #f.close()

      model_params = permutations_runner.runWithConfig(swarm_config, {'maxWorkers': 8})
      # TODO do something with this result, with maybe a callback or something
      model = ModelFactory.create(model_params)




