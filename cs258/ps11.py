from queue_test import *


def test():
    # Try a zero-length queue.
    q = Queue(0)
    assert q.empty()
    assert q.full()
    assert None == q.dequeue()
    assert q.enqueue(1) is False

    q = Queue(1)
    assert q.empty()
    assert not q.full()
    assert None == q.dequeue()
    assert q.enqueue(1)
    assert not q.empty()
    val = q.dequeue()
    assert val == 1

    # Try a longer integer
    q.enqueue(2 ** 16)
    val = q.dequeue()
    assert val == 2 ** 16

    # Try a long queue
    q = Queue(100)
    for i in range(99):
        q.enqueue(i)
        assert not q.empty()
        assert not q.full()
    q.enqueue(1)
    assert q.full()
    assert not q.empty()
