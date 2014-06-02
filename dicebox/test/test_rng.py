import pytest

from dicebox.rng import logged, uniform, xkcd


class TestRng(object):

    @pytest.fixture
    def start(self):
        return 1

    @pytest.fixture
    def end(self):
        return 20

    @pytest.fixture
    def rolls(self):
        return 5

    def test_uniform(self, start, end):
        assert type(uniform(start, end)) == int

    def test_xkcd(self, start, end):
        assert type(xkcd(start, end)) == int

    def test_logged(self, start, end, rolls):
        log = []
        logged_rng = logged(uniform, log)
        result = [logged_rng(start, end) for i in range(rolls)]
        assert result == log
