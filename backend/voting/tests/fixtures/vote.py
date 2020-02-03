import math
import random

import pytest
from voting.models import Vote


def get_random_vote():
    return math.floor(random.uniform(Vote.VALUES.not_interested, Vote.VALUES.must_see))


@pytest.fixture
def random_vote():
    def wrapper():
        return get_random_vote()

    return wrapper
