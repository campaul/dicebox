from dicebox import random


class DiceFactory(object):

    def __init__(self):
        self.rng = random.uniform

    def __call__(self, count):
        return Die(count, self.rng)


class Die(object):

    def __init__(self, count, rng=random.uniform):
        super(Die, self).__init__()
        self.count = count
        self.rng = rng

    def each(self):
        return self.rng(1, self.count)

    def __mul__(self, count):
        return Pool(self, int(count))

    def __rmul__(self, count):
        return self.__mul__(count)

    def __add__(self, count):
        return Add(self, int(count))

    def __sub__(self, count):
        return Add(self, -int(count))

    def __call__(self):
        return self.each()

    def __int__(self):
        return self.each()


class Modifier(Die):

    def __init__(self, item, count):
        super(Modifier, self).__init__(count)
        self.item = item

    def __int__(self):
        return sum([int(item) for item in self.each()])


class Pool(Modifier):

    def each(self):
        return [self.item.each() for i in range(self.count)]

    def __rshift__(self, count):
        return Best(self, int(count))

    def __lshift__(self, count):
        return Worst(self, int(count))


class Add(Modifier):

    def each(self):
        base = self.item.each()

        if type(base) == int:
            base = [base]

        return base + [self.count]


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
