class serviceLocator(object):
    _container = None

    @staticmethod
    def setServiceLocator(container):
        serviceLocator._container = container

    @staticmethod
    def getService(serviceName):
        return serviceLocator._container[serviceName]()


