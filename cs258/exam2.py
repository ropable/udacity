import array
import random

# Although this specific Queue class has bugs spread
# throughout the code, do not modify the class.
class Queue:

    def __init__(self,size_max):
        assert size_max > 0
        self.max = size_max - 1
        self.head = 0
        self.tail = 0
        self.size = 0
        self.data = array.array('i', range(size_max))

    def empty(self):
        return self.size == 0

    def full(self):
        return self.size == self.max

    def enqueue(self,x):
        x = x % 1000
        self.data[self.tail] = x
        self.size += 1
        self.tail += 1
        if self.tail == self.max:
            self.tail = 0
        return True

    def dequeue(self):
        x = self.data[self.head]
        self.size -= 1
        self.head += 1
        if self.head == self.max:
            self.head = 0
        return x

    def checkRep(self):
        assert self.tail >= 0
        assert self.tail < self.max
        assert self.head >= 0
        assert self.head < self.max
        if self.tail > self.head:
            assert (self.tail-self.head) == self.size
        if self.tail < self.head:
            assert (self.head-self.tail) == (self.max-self.size)
        if self.head == self.tail:
            assert (self.size==0) or (self.size==self.max)

def random_test(reps=10000, q=500):
    q = Queue(q)
    inputs = []
    for i in range(reps):
        randint = random.randrange(10000)
        if (random.random() > q.size/float(q.max)):
            try:
                q.enqueue(randint)
                q.checkRep()
                inputs.append((randint, 0))
            except:
                inputs.append((randint, 1))
        else:
            try:
                q.dequeue()
                q.checkRep()
                inputs.append(('dq', 0))
            except:
                inputs.append(('dq', 1))
    return inputs
