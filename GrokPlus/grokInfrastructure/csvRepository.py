import csv
import os

class csvRepository(object):
    def __init__(self, csvFileLocation):
        self._csvFileLocation = csvFileLocation

    def put(self, matrix, uniqueLocation):
        filename = os.path.join(uniqueLocation, self._csvFileLocation)
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        with open(filename, "wb") as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(matrix)