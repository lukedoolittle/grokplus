import sys
import os

from nupic.swarming import permutations_runner

class nupicAdapter(object):
    def __init__(self):
        pass

    def permutations_runner(self, filepath):
      fileArgPath = os.path.expanduser(filepath)
      fileArgPath = os.path.expandvars(fileArgPath)
      fileArgPath = os.path.abspath(fileArgPath)

      permWorkDir = os.path.dirname(fileArgPath)

      outputLabel = os.path.splitext(os.path.basename(fileArgPath))[0]

      basename = os.path.basename(fileArgPath)
      fileExtension = os.path.splitext(basename)[1]
      optionsDict = {'maxWorkers' : 4}

      return permutations_runner.runWithJsonFile(fileArgPath, optionsDict, outputLabel, permWorkDir)




