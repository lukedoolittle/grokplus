import json
from couchbase.views.params import Query

class repository(object):
    def __init__(self, couchbaseBucket, designDocument):
        self.bucket = couchbaseBucket
        self.designDocument = designDocument

    def put(self, object, id):
        self.bucket.insert(id.urn[9:], json.loads(object))

    def putJson(self, json, id):
        self.bucket.insert(id.urn[9:], json)

    def get(self, id):
        result = bucket.get(id)
        return result.value; 

    def getByView(self, viewName, parameter):
        options = Query()
        options.mapkey_range = (str(parameter), str(parameter))
        options.stale = False
        rows = self.bucket.query(self.designDocument, viewName, query=options)
        # the resulting row view from bucket.query is [key, value, docid, doc]
        # since we want docids, select the elements with index 2
        docids = [row[2] for row in rows]
        results = self.bucket.get_multi(docids).values()
        return [result.value for result in results]