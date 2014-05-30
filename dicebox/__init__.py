from contextlib import contextmanager
from dicebox.dice import DiceFactory

d = DiceFactory()

@contextmanager
def bias(d, rng):
    rng, d.rng = d.rng, rng
    yield
    d.rng = rng
