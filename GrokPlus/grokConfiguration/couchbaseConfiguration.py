from couchbase.bucket import Bucket
from couchbase.exceptions import HTTPError
from couchbase.bucket import Bucket

class couchbaseConfiguration(object):
    def __init__(self, designDocumentName, bucketUrl):
        self.designDocumentName = designDocumentName
        self._bucketUrl = bucketUrl

    def createMapView(self, viewName, mapFunction, reduceFunction):
        bucket = Bucket(self._bucketUrl)
        try:
            designDocument = bucket.design_get(self.designDocumentName, False)
            self._createView(designDocument.value, viewName, mapFunction, reduceFunction)
        except HTTPError:
            designDocument = { 'views': {} }
            self._createView(designDocument, viewName, mapFunction, reduceFunction)

    def _createView(self, designDocument, viewName, mapFunction, reduceFunction):
        bucket = Bucket(self._bucketUrl)
        if reduceFunction == None:
            designDocument['views'][viewName] = { 'map': mapFunction }
        else:
            designDocument['views'][viewName] = { 'map': mapFunction, 'reduce': reduceFunction }
        bucket.design_create(self.designDocumentName, designDocument, False, 10000)


