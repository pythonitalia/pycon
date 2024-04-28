import math
import random

import pytest
from voting.models import Vote


def get_random_vote():
    return math.floor(random.uniform(Vote.Values.not_interested, Vote.Values.must_see))


@pytest.fixture
def random_vote():
    def wrapper():
        return get_random_vote()

    return wrapper
