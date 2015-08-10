import sys

from grokConfiguration.bootstrap import bootstrap
from grokConfiguration.serviceLocator import serviceLocator

def main (subscriber):
    subscriber.subscribe("MetricCreated")
    subscriber.subscribe("EncodingCreated")

    print("subscriber running...")
    subscriber.run()

if __name__ == '__main__':
    bootstrap().run()
    serviceLocator.getService('espresso').run()
    main(serviceLocator.getService('subscriber'))


