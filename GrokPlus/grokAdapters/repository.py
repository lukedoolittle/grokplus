import json

from couchbase.views.params import Query

class repository(object):
    def __init__(self, couchbaseBucketGenerator, designDocument):
        self._bucketGenerator = couchbaseBucketGenerator
        self.designDocument = designDocument

    def put(self, object, id):
        bucket = self._bucketGenerator()
        bucket.insert(id.urn[9:], json.loads(object))

    def putJson(self, json, id):
        bucket = self._bucketGenerator()
        bucket.insert(id.urn[9:], json)

    def get(self, id):
        bucket = self._bucketGenerator()
        result = bucket.get(id)
        return result.value; 

    def getByView(self, viewName, parameter):
        bucket = self._bucketGenerator()
        options = Query()
        options.mapkey_range = (str(parameter), str(parameter))
        options.stale = False
        rows = bucket.query(self.designDocument, viewName, query=options)
        # the resulting row view from bucket.query is [key, value, docid, doc]
        # since we want docids, select the elements with index 2
        docids = [row[2] for row in rows]
        if len(docids) == 0:
            return []
        results = bucket.get_multi(docids).values()
        return [result.value for result in results]