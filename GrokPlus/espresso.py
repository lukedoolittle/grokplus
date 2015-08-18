from grokFramework.jsonPayload import fileToJson

import binascii
import os
import sys
import datetime

import zmq
from zmq.devices import monitored_queue
from threading import Thread

class espresso(object):
    def __init__(self, subscriberPort, publisherPort):
        self._subscriberPort = subscriberPort
        self._publisherPort = publisherPort

    def zpipe(self, ctx):
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

    def listener_thread (self, pipe):

        # Print everything that arrives on pipe
        while True:
            try:
                print (str(datetime.datetime.now()) + " " + str(pipe.recv_multipart()))
            except zmq.ZMQError as e:
                if e.errno == zmq.ETERM:
                    break           # Interrupted

    def startBroker(self):

        # Start child threads
        ctx = zmq.Context.instance()

        pipe = self.zpipe(ctx)

        print ("broker binding to subscriber port " + self._subscriberPort)
        subscriber = ctx.socket(zmq.XSUB)
        subscriber.bind("tcp://*:" + self._subscriberPort)

        print ("broker binding to publisher port " + self._publisherPort)
        publisher = ctx.socket(zmq.XPUB)
        publisher.bind("tcp://*:" + self._publisherPort)

        l_thread = Thread(target=self.listener_thread, args=(pipe[1],))
        l_thread.start()

        print("Broker online...")
        try:
            monitored_queue(subscriber, publisher, pipe[0], 'pub', 'sub')
        except KeyboardInterrupt:
            print ("Interrupted")

        del subscriber, publisher, pipe
        ctx.term()

if __name__ == '__main__':
    configuration = fileToJson('config.json')
    espresso(configuration['publisherPort'], configuration['subscriberPort']).startBroker()
