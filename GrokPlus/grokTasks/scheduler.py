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

    def cancel(self):
        self.finished.set()

    def run(self):
        print("running a new job...")
        while self.resetted:
            self.resetted = False
            self.finished.wait(self.interval)

        if not self.finished.isSet():
            print("calling function for a job...")
            self.finished.set()
            self.function(self.arg)
        
    def reset(self, interval = None):
        if interval:
            self.interval = interval
        
        print ("job reset")
        self.resetted = True
        self.finished.set()
        self.finished.clear()

class scheduler(object):
    def __init__(self, invokeDelay):
        self._invokeDelay = invokeDelay
        self._lock = Lock()
        self._jobs = {}

    def addNew(self, personId, function):
        self._lock.acquire()
        try:
            if self._jobs.get(personId, None) == None:
                newJob = job(self._invokeDelay, function, personId)    
                newJob.run()
                self._jobs[personId] = newJob
        finally:
            self._lock.release()
    
    def reset(self, personId):
        if self._jobs.get(personId, None) != None:
            self._jobs[personId].reset()