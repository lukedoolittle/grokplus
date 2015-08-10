class mockRepository(object):
    def put(self, object, id):
        print("id = " + id.urn[9:])
        print("object = " + str(object))
