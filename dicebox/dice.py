import random


class Die(object):

    def __init__(self, count):
        super(Die, self).__init__()
        self.count = count

    def each(self):
        return random.randint(1, self.count)

    def __mul__(self, count):
        return Pool(self, count)

    def __rmul__(self, count):
        return self.__mul__(count)

    def __add__(self, count):
        return Add(self, count)

    def __sub__(self, count):
        return Add(self, -count)

    def __call__(self):
        return self.each()


class Pool(Die):

    def __init__(self, item, count):
        super(Pool, self).__init__(count)
        self.item = item

    def each(self):
        return [self.item.each() for i in range(self.count)]

    def __rshift__(self, count):
        return Best(self, count)

    def __lshift__(self, count):
        return Worst(self, count)


class Add(Pool):

    def each(self):
        return self.item.each() + [self.count]


class Sort(Pool):

    def each(self):
        return sorted(self.item.each(), key=self.sum_each)

    def sum_each(self, item):
        sum = 0

        if type(item) != list:
            return item

        for i in item:
            sum = sum + self.sum_each(i)

        return sum


class Best(Sort):

    def each(self):
        return super(Best, self).each()[-self.count:]


class Worst(Sort):

    def each(self):
        return super(Worst, self).each()[:self.count]
