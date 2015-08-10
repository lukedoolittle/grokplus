import sys
import os

#from nupic.swarming import permutations_runner

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

      #run this in a thread
      #also can use runWithConfig to dodge having to write the json configuration to a file
      f = open('out.txt', 'w')
      permutations_runner.runWithJsonFile(fileArgPath, optionsDict, outputLabel, permWorkDir) >> 'Filename:', filename  # or f.write('...\n')
      f.close()




