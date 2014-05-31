import mock
import pytest

from dicebox.dice import Add, Best, Die, DiceFactory, Modifier, Pool, Sort, Worst


class TestDiceFactory(object):

    @pytest.fixture
    def sides(self):
        return 20

    def test_call(self, sides):
        assert type(DiceFactory()(sides)) == Die

    def test_bias(self, sides):
        rng = mock.Mock()
        factory = DiceFactory()

        with factory.bias(rng):
            factory(20)()

        rng.assert_called_with(1, 20)


class TestDie(object):

    @pytest.fixture
    def count(self):
        return 5

    @pytest.fixture
    def die(self, rng):
        return Die(20, rng)

    @pytest.fixture
    def random(self):
        return 4

    @pytest.fixture
    def rng(self, random):
        return mock.Mock(return_value=random)

    def test_call(self, die, random, rng):
        assert die() == random
        rng.assert_called_with(1, 20)

    def test_each(self, die, random, rng):
        assert die.each() == random
        rng.assert_called_with(1, 20)

    def test_mul(self, count, die, random):
        pool = die * count
        assert pool.each() == [random for i in range(count)]

    def test_rmul(self, count, die, random):
        pool = count * die
        assert pool.each() == [random for i in range(count)]

    def test_add(self, count, die):
        pool = die + count
        assert pool.each() == [die.each(), count]

    def test_sub(self, count, die):
        pool = die - count
        assert pool.each() == [die.each(), -count]

    def test_int(self, die, random):
        assert int(die) == random


class TestModifier(object):

    randoms = None

    def log_random(self, r):
        if self.randoms is None:
            self.randoms = []

        self.randoms.append(r)
        return r

    @pytest.fixture
    def count(self):
        return 5

    @pytest.fixture
    def rng_value(self):
        return 4

    @pytest.fixture
    def rng(self, rng_value):
        return lambda start, finish: self.log_random(rng_value)

    @pytest.fixture
    def die(self, rng):
        return Die(20, rng)

    @pytest.fixture
    def modifier(self, die, count):
        return Modifier(die, count)

    def test_each(self, modifier, count):
        assert modifier.each() == self.randoms

    def test_int(self, modifier, rng_value, count):
        assert int(modifier) == sum(self.randoms)


class TestPool(TestModifier):

    @pytest.fixture
    def rng(self):

        def rng(start, end):
            if self.randoms is None:
                return self.log_random(1)
            else:
                return self.log_random(self.randoms[-1] + 1)

        return rng

    @pytest.fixture
    def modifier(self, die, count):
        return Pool(die, count)

    def test_rshift(self, modifier):
        assert (modifier >> 2).each() == [4, 5]

    def test_lshift(self, modifier):
        assert (modifier << 2).each() == [1, 2]


class TestAdd(TestModifier):

    @pytest.fixture
    def modifier(self, die, count):
        return Add(die, count)

    def test_each(self, modifier, count):
        assert modifier.each() == self.randoms + [count]

    def test_int(self, modifier, count):
        assert int(modifier) == sum(self.randoms + [count])


class TestSort(TestModifier):

    @pytest.fixture
    def modifier(self, die, count):
        return Sort(Pool(die, count), None)

    def test_each(self, modifier):
        assert modifier.each() == sorted(self.randoms)

    def result(self):
        return sorted(self.randoms)

    def test_each(self, modifier):
        assert modifier.each() == self.result()

    def test_int(self, modifier):
        assert int(modifier) == sum(self.result())


class TestBest(TestSort):

    @pytest.fixture
    def modifier(self, die, count):
        return Best(Pool(die, count), count - 1)

    def result(self):
        return sorted(self.randoms)[1:]


class TestWorst(TestSort):

    @pytest.fixture
    def modifier(self, die, count):
        return Worst(Pool(die, count), count - 1)

    def result(self):
        return sorted(self.randoms)[:-1]
