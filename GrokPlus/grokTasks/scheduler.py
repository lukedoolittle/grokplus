from threading import Thread, Lock, Event, Timer
import time

class job(Thread):
    def __init__(self, interval, function, arg):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.arg = arg
        self.finished = Event()
        self.resetted = True
        self.cancelled = False

    def cancel(self):
        print("thread cancelled")
        self.cancelled = True
        self.finished.set()

    def run(self):
        timeout = False
        while self.resetted and not self.cancelled and not timeout:
            print("restarting timer loop")
            self.resetted = False
            timeout = not self.finished.wait(self.interval)

        print("through timer loop with timeout " + str(timeout))

        if timeout:
            print("running scheduled function")
            self.function(self.arg)
        self.finished.set()
        
    def reset(self, interval = None):
        if interval:
            self.interval = interval
        
        print("reset called")
        self.resetted = True
        self.finished.set()
        self.finished.clear()

class scheduler(object):
    def __init__(self, invokeDelay):
        self._invokeDelay = invokeDelay
        self._lock = Lock()
        self._jobs = {}

    def createJobIfNew(self, personId, function):
        self._lock.acquire()
        try:
            if self._jobs.get(personId, None) == None:
                newJob = job(self._invokeDelay, function, personId)    
                newJob.start()
                self._jobs[personId] = newJob
        finally:
            self._lock.release()
    
    def reset(self, personId):
        if self._jobs.get(personId, None) != None:
            self._jobs[personId].reset()