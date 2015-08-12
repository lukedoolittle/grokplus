from threading import Thread, Lock, Event, Timer

if __name__ == '__main__':
    testEvent = Event()
    testEvent.set()
    timeout = not testEvent.wait(100)
    print("timeout returned when event is set is " + str(timeout))


