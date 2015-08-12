import json

def fileToJson(filename):
        with open(filename, "r") as data_file:    
            data = data_file.read().replace('\n', '').replace("\xEF", "").replace("\xBB", "").replace("\xBF", "")
        return json.loads(data)
