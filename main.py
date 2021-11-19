import heapq
import sys

import events


def print_sim(time, event_name, population):
    year = time / 12
    alive = [p for p in population if p.is_alive]
    dead = [p for p in population if not p.is_alive]
    print(f"Year: {year} Month: {time}")
    print(f"Event: {event_name}")
    print()
    print(f"Alive Count: {len(alive)}")
    print(f"Men Count: {len([p for p in alive if not p.is_woman])}")
    print(f"Women Count: {len([p for p in alive if p.is_woman])}")
    print()
    print(f"Dead Count: {len(dead)}")
    print(f"Men Count: {len([p for p in dead if not p.is_woman])}")
    print(f"Women Count: {len([p for p in dead if p.is_woman])}")
    print("----------------------------------------------------")


def simulate(sim_time, men, women):
    time, population = 0, []
    event_queue = (
        [(time, "new_person", (False, None))] * men
        + [(time, "new_person", (True, None))] * women
        + [(time + 1, "look_for_matches", ())]
    )
    heapq.heapify(event_queue)

    while time <= sim_time and (time == 0 or len([p for p in population if p.is_alive])):
        etime, event_name, args = heapq.heappop(event_queue)
        event_func = getattr(events, event_name)
        for p in population:
            p.age += etime - time
        time = etime
        event_func(time, event_queue, population, args)

        print_sim(time, event_name, population)


if __name__ == "__main__":
    simulate(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
