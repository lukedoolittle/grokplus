import binascii
import os
import sys

import zmq
from zmq.devices import monitored_queue

class espresso(object):
    def __init__(self, subscriberPort, publisherPort):
        self._subscriberPort = subscriberPort
        self._publisherPort = publisherPort

    def run(self):
        l_thread = Thread(target=runBroker, args=(self._subscriberPort, self._publisherPort))
        l_thread.start()

    def zpipe(ctx):
        """build inproc pipe for talking to threads
        mimic pipe used in czmq zthread_fork.
        Returns a pair of PAIRs connected via inproc
        """
        a = ctx.socket(zmq.PAIR)
        b = ctx.socket(zmq.PAIR)
        a.linger = b.linger = 0
        a.hwm = b.hwm = 1
        iface = "inproc://%s" % binascii.hexlify(os.urandom(8))
        a.bind(iface)
        b.connect(iface)
        return a,b

    def listener_thread (pipe):

        # Print everything that arrives on pipe
        while True:
            try:
                print (pipe.recv_multipart())
            except zmq.ZMQError as e:
                if e.errno == zmq.ETERM:
                    break           # Interrupted

    def runBroker (subscriberPort, publisherPort):

        # Start child threads
        ctx = zmq.Context.instance()

        pipe = zpipe(ctx)

        print("Connecting subscriber to port " + subscriberPort)
        subscriber = ctx.socket(zmq.XSUB)
        subscriber.connect("tcp://localhost:" + subscriberPort)

        print("Connecting publisher to port " + publisherPort)
        publisher = ctx.socket(zmq.XPUB)
        publisher.bind("tcp://*:" + publisherPort)

        print("Starting listener...")
        l_thread = Thread(target=listener_thread, args=(pipe[1],))
        l_thread.start()

        print("Monitoring queue...")
        try:
            monitored_queue(subscriber, publisher, pipe[0], 'pub', 'sub')
        except KeyboardInterrupt:
            print ("Interrupted")

        del subscriber, publisher, pipe
        ctx.term()


