import mock
import pytest

from dicebox.dice import Die, DiceFactory, Pool


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
