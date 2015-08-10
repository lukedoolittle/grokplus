from couchbase.bucket import Bucket
from couchbase.exceptions import HTTPError

class couchbaseConfiguration(object):
    def __init__(self, bucket, designDocumentName):
        self.bucket = bucket
        self.designDocumentName = designDocumentName

    def createMapView(self, viewName, mapFunction):
        try:
            designDocument = self.bucket.design_get(self.designDocumentName, False)
            designDocument.value['views'][viewName] = { 'map': mapFunction }
            self.bucket.design_create(self.designDocumentName, designDocument.value, False, 10000)
        except HTTPError:
            designDocument = { 'views': {} }
            designDocument['views'][viewName] = { 'map': mapFunction }
            self.bucket.design_create(self.designDocumentName, designDocument, False, 10000)

