from threading import Thread

import zmq
import uuid
import json

class zmqProxy(object):
    def __init__(self, port, repository, scheduler, callback):
        ctx = zmq.Context.instance()
        self._subscriber = ctx.socket(zmq.SUB)
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
                self._repository.put(message, uuid.uuid4())
                personId = json.loads(message)["personId"]
                self._scheduler.createJobIfNew(personId, self._callback)
            except zmq.ZMQError as e:
                if e.errno == zmq.ETERM:
                    break           # Interrupted
                else:
                    raise



