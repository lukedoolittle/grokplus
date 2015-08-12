from threading import Thread

import zmq
import uuid
import json

class zmqAdapter(object):
    def __init__(self, port, repository, scheduler, callback):
        ctx = zmq.Context.instance()
        self._subscriber = ctx.socket(zmq.SUB)
        print ("Adapter connecting to subscriber port " + port)
        self._subscriber.connect("tcp://localhost:" + port)
        self._repository = repository
        self._scheduler = scheduler
        self._callback = callback

    def subscribe(self, message):
        self._subscriber.setsockopt(zmq.SUBSCRIBE, message)

    def run(self):
        print 
        while True:
            try:
                message = self._subscriber.recv_multipart()[1]
                self._putMessage(message)
                #processThread = Thread(target=self._putMessage, args=[message])
                #processThread.start();

            except zmq.ZMQError as e:
                if e.errno == zmq.ETERM:
                    break           # Interrupted
                else:
                    raise
    
    #TODO this should be factored out 
    def _putMessage(self, message):
        self._repository.put(message, uuid.uuid4())
        personId = json.loads(message)["personId"]
        self._scheduler.createJobIfNew(personId, self._callback)
        self._scheduler.reset(personId)


