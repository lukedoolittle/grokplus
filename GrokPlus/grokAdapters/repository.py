﻿import json

from couchbase.views.params import Query
from couchbase.bucket import Bucket

class repository(object):
    def __init__(self, bucketUrl, designDocument):
        self._bucketUrl = bucketUrl
        self.designDocument = designDocument

    def put(self, object, id):
        bucket = Bucket(self._bucketUrl)
        bucket.insert(id.urn[9:], json.loads(object))

    def putJson(self, json, id):
        bucket = Bucket(self._bucketUrl)
        bucket.insert(id.urn[9:], json)

    def get(self, id):
        bucket = Bucket(self._bucketUrl)
        result = bucket.get(id)
        return result.value; 

    def getByView(self, viewName, parameter):
        bucket = Bucket(self._bucketUrl)
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
