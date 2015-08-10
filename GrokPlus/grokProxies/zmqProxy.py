import zmq
import uuid

class zmqProxy(object):
    def __init__(self, port, repository):
        ctx = zmq.Context.instance()
        self.subscriber = ctx.socket(zmq.SUB)
        self.subscriber.connect("tcp://localhost:" + port)
        self.repository = repository

    def subscribe(self, message):
        self.subscriber.setsockopt(zmq.SUBSCRIBE, message)

    def run(self):
        while True:
            try:
                msg = self.subscriber.recv_multipart()
                self.repository.put(msg[1], uuid.uuid4())
            except zmq.ZMQError as e:
                if e.errno == zmq.ETERM:
                    break           # Interrupted
                else:
                    raise


