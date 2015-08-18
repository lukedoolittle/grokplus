import sys
from threading import Thread

from grokConfiguration.bootstrap import bootstrap
from grokConfiguration.serviceLocator import serviceLocator

def main (subscriber):
    subscriber.subscribe("MetricCreated")
    subscriber.subscribe("EncodingCreated")

    print("Subscriber running...")
    subscriber.run()

if __name__ == '__main__':
    bootstrap().run()
    main(serviceLocator.getService('subscriber'))