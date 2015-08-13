from couchbase.bucket import Bucket
from couchbase.exceptions import HTTPError

class couchbaseConfiguration(object):
    def __init__(self, bucket, designDocumentName):
        self.bucket = bucket
        self.designDocumentName = designDocumentName

    def createMapView(self, viewName, mapFunction, reduceFunction):
        try:
            designDocument = self.bucket.design_get(self.designDocumentName, False)
            self._createView(designDocument.value, viewName, mapFunction, reduceFunction)
        except HTTPError:
            designDocument = { 'views': {} }
            self._createView(designDocument, viewName, mapFunction, reduceFunction)

    def _createView(self, designDocument, viewName, mapFunction, reduceFunction):
        if reduceFunction == None:
            designDocument['views'][viewName] = { 'map': mapFunction }
        else:
            designDocument['views'][viewName] = { 'map': mapFunction, 'reduce': reduceFunction }
        self.bucket.design_create(self.designDocumentName, designDocument, False, 10000)


