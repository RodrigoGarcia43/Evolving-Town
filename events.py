import heapq
import random

import aux


class Person(object):
    def __init__(
        self,
        age: int,
        children_left: int,
        is_woman: bool,
    ) -> None:
        self.age = age
        self.is_alive = True
        self.partner = None
        self.is_waiting = False
        self.children_left = children_left
        self.is_pregnant = False
        self.is_woman = is_woman

    # just for the heapq to work
    def __lt__(self, _):
        return False


def new_person(time, events, population, args):
    is_woman, age = args
    age = int(random.uniform(0, 100 * 12)) if age is None else age
    person = Person(age, aux.get_max_children(), is_woman)
    population.append(person)

    death_top = aux.get_death_range(person)
    death_age = int(random.uniform(person.age, death_top * 12))
    print("death to", death_top, death_age, person.age)
    heapq.heappush(events, (time + (death_age - age), "death", (person,)))


def death(time, events, population, args):
    (person,) = args
    person.is_alive = False
    if person.partner is not None and person.partner.is_alive:
        heapq.heappush(events, (time, "widow", (person.partner,)))


def matching(time, events, population, args):
    person1, person2 = args
    person1.partner = person2
    person2.partner = person1
    if aux.is_breakup():
        heapq.heappush(
            events,
            (int(random.uniform(time + 1, time + 5000)), "breakup", (person1, person2)),
        )
    (man, woman) = person1, person2 if person1.is_woman else (person2, person1)
    heapq.heappush(
        events,
        (int(time), "try_pregnant", (man, woman)),
    )


def try_pregnant(time, events, population, args):
    man, woman = args
    if man.partner != woman:
        return

    if (
        not woman.is_pregnant
        and man.children_left > 0
        and woman.children_left > 0
        and aux.gets_pregnant(woman)
    ):
        woman.is_pregnant = True
        heapq.heappush(events, (time + 9, "give_birth", (man, woman)))
    else:
        heapq.heappush(
            events,
            (time + 2, "try_pregnant", (man, woman)),
        )


def breakup(time, events, population, args):
    p1, p2 = args
    if not p1.is_alive or not p2.is_alive:
        return
    p1.is_waiting = True
    p2.is_waiting = True
    heapq.heappush(events, (time + aux.get_wait_time(p1), "waiting_over", (p1)))
    heapq.heappush(events, (time + aux.get_wait_time(p2), "waiting_over", (p2)))


def widow(time, events, population, args):
    (person,) = args
    if not person.is_alive:
        return
    heapq.heappush(
        events, (time + aux.get_wait_time(person), "waiting_over", (person,))
    )


def waiting_over(time, events, population, args):
    (person,) = args
    person.is_waiting = False


def give_birth(time, events, population, args):
    (man, woman) = args
    if not woman.is_alive:
        return

    if man.is_alive:
        man.children_left -= aux.get_children_count()

    woman.children_left -= aux.get_children_count()

    heapq.heappush(events, (time, "new_person", (aux.is_girl, 0)))


def look_for_matches(time, events, population, args):
    looking = [
        person
        for person in population
        if person.is_alive
        and person.partner is None
        and not person.is_waiting
        and aux.is_looking(person)
    ]

    matched = [False] * len(looking)
    for (i, p1) in enumerate(looking):
        for (j, p2) in enumerate(looking):
            if (
                not matched[i]
                and not matched[j]
                and p1.is_woman != p2.is_woman
                and aux.is_matching(p1, p2)
            ):
                heapq.heappush(events, (time, "matching", (p1, p2)))
                matched[i] = matched[j] = True

    heapq.heappush(events, (time + 1, "look_for_matches", ()))
