import sys
from threading import Thread

from grokConfiguration.bootstrap import bootstrap
from grokConfiguration.serviceLocator import serviceLocator

def main (subscriber):
    subscriber.subscribe("MetricCreated")
    subscriber.subscribe("EncodingCreated")

    print("subscriber running...")
    subscriber.run()

if __name__ == '__main__':
    bootstrap().run()

    espresso = serviceLocator.getService('espresso')
    print("starting espresso on a thread...")
    Thread(target=espresso.startBroker).start()

    main(serviceLocator.getService('subscriber'))


