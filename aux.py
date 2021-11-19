import math
import random

looking = {
    (0, 12): 0,
    (12, 15): 0.6,
    (15, 21): 0.65,
    (21, 35): 0.8,
    (35, 45): 0.6,
    (45, 60): 0.5,
    (60, 125): 0.2,
}


def is_looking(p):
    age = p.age / 12
    prob = next(
        prob for ((minim, maxim), prob) in looking.items() if minim <= age < maxim
    )
    return random.uniform(0, 1) < prob


matching = {
    (0, 5): 0.45,
    (5, 10): 0.4,
    (10, 15): 0.35,
    (15, 20): 0.25,
    (20, 125): 0.15,
}


def is_matching(p1, p2):
    age_gap = abs(p1.age - p2.age) / 12
    prob = next(
        prob for ((minim, maxim), prob) in matching.items() if minim <= age_gap < maxim
    )
    return random.uniform(0, 1) < prob


max_children = {0.6: 1, 0.75: 2, 0.35: 3, 0.2: 4, 0.1: 5, 0.05: 100}


def get_max_children():
    u = random.uniform(0, 1)
    _max_children = sorted(max_children)
    for item in _max_children:
        if u < item:
            return max_children[item]
        u = u - item
    return 100


death = {
    (0, 12): (0.25, 0.25),
    (12, 45): (0.1, 0.15),
    (45, 76): (0.3, 0.35),
    (76, 125): (0.7, 0.65),
}


def get_death_range(p):
    age = p.age / 12
    for ((minim, maxim), (man, woman)) in death.items():
        if minim > age or age > maxim:
            continue
        if p.is_woman:
            prob = woman
        else:
            prob = man
        if random.uniform(0, 1) < prob:
            return maxim
    return 125


def is_girl():
    return random.uniform(0, 1) <= 0.5


pregnancy = {
    (0, 12): 0,
    (12, 15): 0.2,
    (15, 21): 0.45,
    (21, 35): 0.8,
    (35, 45): 0.4,
    (45, 60): 0.2,
    (60, 125): 0.05,
}


def gets_pregnant(p):
    age = p.age / 12
    prob = next(
        probability
        for ((minim, maxim), probability) in pregnancy.items()
        if minim <= age < maxim
    )
    return random.uniform(0, 1) < prob


wait_time_lambda = {
    (0, 12): 0,
    (12, 15): 3,
    (15, 21): 6,
    (21, 35): 6,
    (35, 45): 12,
    (45, 60): 24,
    (60, 125): 48,
}


def get_wait_time(p):
    age = p.age / 12
    _lambda = next(
        _lambda
        for ((minim, maxim), _lambda) in wait_time_lambda.items()
        if minim <= age < maxim
    )

    return int(-(1 / _lambda) * math.log(random.random()))


children_count = {0.7: 1, 0.18: 2, 0.08: 3, 0.04: 4, 0.02: 5}


def get_children_count():
    u = random.random()
    for item in sorted(children_count):
        if u < item:
            return children_count[item]
        u = u - item
    return 5


def is_breakup():
    return random.uniform(0, 1) <= 0.2
