import random

def uniform(start, end):
    return random.randint(start, end)

def xkcd(start, end):
    return 4

def logged(rng, log):

    def logged_rng(start, end):
        result = rng(start, end)
        log.append(result)
        return result

    return logged_rng
