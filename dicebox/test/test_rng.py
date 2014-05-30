import pytest

from dicebox.rng import uniform, xkcd


class TestRng(object):

    @pytest.fixture
    def start(self):
        return 1

    @pytest.fixture
    def end(self):
        return 20

    def test_uniform(self, start, end):
        assert type(uniform(start, end)) == int

    def test_xkcd(self, start, end):
        assert type(xkcd(start, end)) == int
