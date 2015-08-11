import json

class jsonPayload(object):
    def __init__(self, dict):
        vars(self).update( dict )

def fileToJson(filename):
        with open(filename, "r") as data_file:    
            data = data_file.read().replace('\n', '').replace("\xEF", "").replace("\xBB", "").replace("\xBF", "")
        return json.loads( data, object_hook = jsonPayload)
