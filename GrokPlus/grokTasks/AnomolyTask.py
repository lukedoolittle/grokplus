class anomolyTask(object):
    def __init__(self, repository, nupic):
        self._repository = repository
        self._nupic = nupic

    def run(self, personId):
        self._nupic.create_model()

