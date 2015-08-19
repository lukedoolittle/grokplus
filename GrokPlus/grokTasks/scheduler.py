from threading import Thread, Lock, Event, Timer
import time

class job(Thread):        
        def __init__(self, interval, function, arg):
            Thread.__init__(self)
            self.interval = interval
            self.function = function
            self.arg = arg
            self.finished = Event()

        def run(self):
            while True:
                self.finished.wait(self.interval)
                if self.finished.is_set():
                    break
                self.function(self.arg)

        def cancel(self):
            self.finished.set()

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