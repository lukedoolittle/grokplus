import json

from couchbase.views.params import Query
from couchbase.bucket import Bucket
from couchbase.exceptions import NotFoundError

class repository(object):
    def __init__(self, bucketUrl, designDocument, viewName):
        self._bucketUrl = bucketUrl
        self.designDocument = designDocument
        self._viewName = viewName

    def put(self, object, id):
        bucket = Bucket(self._bucketUrl)
        bucket.insert(id.urn[9:], json.loads(object))

    def putJson(self, json, id):
        bucket = Bucket(self._bucketUrl)
        bucket.insert(str(id), json)

    def get(self, id):
        bucket = Bucket(self._bucketUrl)
        try:
            result = bucket.get(id)
            return result.value 
        except NotFoundError:
            return None
        

    def getByView(self, parameter):
        bucket = Bucket(self._bucketUrl)
        options = Query()
        options.mapkey_range = (str(parameter), str(parameter))
        options.stale = False
        rows = bucket.query(self.designDocument, self._viewName, query=options)
        # the resulting row view from bucket.query is [key, value, docid, doc]
        # since we want docids, select the elements with index 2
        docids = [row[2] for row in rows]
        if len(docids) == 0:
            return []
        results = bucket.get_multi(docids).values()
        return [result.value for result in results]
