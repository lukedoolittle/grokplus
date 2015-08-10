from grokAdapters.repository import repository
from grokConfiguration.couchbaseConfiguration import couchbaseConfiguration
from couchbase.bucket import Bucket
from grokTasks.learningTask import learningTask
import uuid
import time
import csv

#class repositoryTests(object):
#    designDocumentName = "someDesignDocument"
#    myBucket = Bucket('couchbase://localhost/default')
    
#    myConfiguration = couchbaseConfiguration(myBucket, designDocumentName)
#    myConfiguration.createMapView("metricsView", "function (doc, meta) {    if (doc.metric && doc.personId && (doc.minValue || doc.minValue === 0) && (doc.maxValue || doc.maxValue === 0)) {        emit(doc.personId, null);    }}")

#    repo = repository(myBucket, designDocumentName)
#    personId = uuid.uuid4()

#    repo.putJson({'metric':'mood', 'personId':personId.urn[9:], 'minValue':0, 'maxValue':5, 'reduce':'sum'}, uuid.uuid4())
#    repo.putJson({'metric':'sleep', 'personId':personId.urn[9:], 'minValue':0, 'maxValue':5, 'reduce':'average'}, uuid.uuid4())
#    repo.putJson({'metric':'steps', 'personId':personId.urn[9:], 'minValue':0, 'maxValue':5, 'reduce':'sum'}, uuid.uuid4())

#    personId = "02b6e5c8-121c-46d7-8e1d-b3f7bd27a254"
#    repo.putJson({'metric':'mood', 'personId':personId, 'minValue':0, 'maxValue':5, 'reduce':'sum'}, uuid.uuid4())
#    repo.putJson({'metric':'sleep', 'personId':personId, 'minValue':0, 'maxValue':5, 'reduce':'average'}, uuid.uuid4())
#    repo.putJson({'metric':'steps', 'personId':personId, 'minValue':0, 'maxValue':5, 'reduce':'sum'}, uuid.uuid4())

#    results = repo.getByView("metricsView", personId);

#    for result in results:
#        print (result['personId'] + " " + result['metric'])

class matrixCreationTests(object):
    designDocumentName = "someDesignDocument"
    myBucket = Bucket('couchbase://localhost/default')
    
    myConfiguration = couchbaseConfiguration(myBucket, designDocumentName)

    print("creating configurations....")
    myConfiguration.createMapView("metricsView", "function (doc, meta) {    if (doc.metric && doc.personId && (doc.minValue || doc.minValue === 0) && (doc.maxValue || doc.maxValue === 0)) {        emit(doc.personId, null);    }}")
    myConfiguration.createMapView("samplesView", "function (doc, meta) {    if (doc.personId && (doc.value || doc.value === 0) && doc.metric && doc.timestamp) {        emit(doc.personId+doc.metric, null);    }}")
    repo = repository(myBucket, designDocumentName)
    personId = uuid.uuid4()

    personId = "02b6e5c8-121c-46d7-8e1d-b3f7bd27a254"
    print("putting metrics....")
    repo.putJson({'metric':'mood', 'personId':personId, 'minValue':-1, 'maxValue':1, 'reduce':'average'}, uuid.uuid4())
    repo.putJson({'metric':'sleep', 'personId':personId, 'minValue':0, 'maxValue':3, 'reduce':'average'}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'minValue':0, 'maxValue':500, 'reduce':'sum'}, uuid.uuid4())

    print("putting moods....")
    repo.putJson({'metric':'mood', 'personId':personId, 'value': .5, 'timestamp': 0}, uuid.uuid4())
    repo.putJson({'metric':'mood', 'personId':personId, 'value': 0, 'timestamp': 1}, uuid.uuid4())
    repo.putJson({'metric':'mood', 'personId':personId, 'value': -.5, 'timestamp': 5}, uuid.uuid4())
    repo.putJson({'metric':'mood', 'personId':personId, 'value': 0, 'timestamp': 7}, uuid.uuid4())
    repo.putJson({'metric':'mood', 'personId':personId, 'value': .5, 'timestamp': 10}, uuid.uuid4())

    print("putting steps....")
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 5, 'timestamp': 0}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 5, 'timestamp': 1}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 10, 'timestamp': 2}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 10, 'timestamp': 3}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 5, 'timestamp': 4}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 5, 'timestamp': 5}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 5, 'timestamp': 6}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 10, 'timestamp': 7}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 10, 'timestamp': 8}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 5, 'timestamp': 9}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 5, 'timestamp': 10}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 5, 'timestamp': 11}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 10, 'timestamp': 12}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 10, 'timestamp': 13}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 5, 'timestamp': 14}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 5, 'timestamp': 15}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 5, 'timestamp': 16}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 10, 'timestamp': 17}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 10, 'timestamp': 18}, uuid.uuid4())
    repo.putJson({'metric':'steps', 'personId':personId, 'value': 5, 'timestamp': 19}, uuid.uuid4())

    print("putting sleeps....")
    repo.putJson({'metric':'sleep', 'personId':personId, 'value': 1, 'timestamp': 7}, uuid.uuid4())
    repo.putJson({'metric':'sleep', 'personId':personId, 'value': 0, 'timestamp': 8}, uuid.uuid4())
    repo.putJson({'metric':'sleep', 'personId':personId, 'value': 0, 'timestamp': 9}, uuid.uuid4())
    repo.putJson({'metric':'sleep', 'personId':personId, 'value': 0, 'timestamp': 10}, uuid.uuid4())
    repo.putJson({'metric':'sleep', 'personId':personId, 'value': 1, 'timestamp': 11}, uuid.uuid4())
    repo.putJson({'metric':'sleep', 'personId':personId, 'value': 0, 'timestamp': 12}, uuid.uuid4())
    repo.putJson({'metric':'sleep', 'personId':personId, 'value': 3, 'timestamp': 13}, uuid.uuid4())

    task = learningTask("", repo, "", "", "")

    print("getting list of metrics....")
    results = repo.getByView("metricsView", personId);

    print("starting to create matrix....")
    matrix = task._createSampleMatrix(results, "sampleView", personId, 0, 20, 2);
    
    metrics = repo.getByView("metricsView", personId)

    metricNames = [metric["metric"] for metric in metrics]
    metricNames.insert(0, "timestamp")
    dataTypes = ["float" for metric in metricNames]
    flags = ["" for metric in metricNames]

    matrix.insert(0, flags)
    matrix.insert(0, dataTypes)
    matrix.insert(0, metricNames)

    with open("somecsvFile.csv", "wb") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(matrix)

if __name__ == '__main__':
    matrixCreationTests()


