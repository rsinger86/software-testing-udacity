from queue_test import *


def test():
    # Only holds 2 byte unsigned ints
    q = Queue(20)
    q.enqueue(100000)
    assert q.dequeue() is 100000
    
    ##### Bug: returns False instead of None when de-queueing empty queue
    q = Queue(1)
    assert q.dequeue() is None
    
    ##### Bug: only stores up to 15 items
    ##### Bug: stores 1 less element than intended
    q = Queue(999999)

    for i in range(0,100):
        assert q.enqueue(i) is True
    
    for i in range(0,100):
        assert q.dequeue() is i

    ### Bug: empty() method calls de-queue and changs state
    q = Queue(1)
    q.enqueue(1)
    q.empty()
    assert q.empty() is False
    