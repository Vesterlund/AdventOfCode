from queue import PriorityQueue
from dataclasses import dataclass, field
from typing import Any

UP, DOWN, RIGHT, LEFT = (0 - 1j), (0 + 1j),  (1 + 0j), (-1 + 0j)

with open("input.txt") as file:
    text = [l.strip() for l in file.readlines()]

tiles = {complex(column, row): int(char) for row, line in enumerate(text) for column, char in enumerate(line)}
END_POSITON = complex(len(text[0]) - 1, len(text) - 1)

@dataclass(order=True)
class PrioritizedItem:
    priority: int
    data: Any=field(compare=False)

def direction_to_int(direction: complex):
    if direction == UP: return 0
    if direction == DOWN:  return 1
    if direction == LEFT: return 2
    else: return 3

def get_best_heat(min_step, max_step):
    dijkstra_imposter = PriorityQueue()
    dijkstra_imposter.put(PrioritizedItem(0, (complex(0, 0), 0, DOWN))) #position, number of straight steps, direction
    dijkstra_imposter.put(PrioritizedItem(0, (complex(0, 0), 0, RIGHT)))

    bests_heats = {key: [[-1] * max_step, [-1] * max_step, [-1] * max_step, [-1] * max_step] for key in tiles.keys()}

    def is_best_heat(steps, position, cost, direction):
        cur_best = bests_heats[position][direction_to_int(direction)][steps - 1]
        if cost < cur_best or cur_best == -1:
            bests_heats[position][direction_to_int(direction)][steps - 1] = cost
            return True

        return False

    while dijkstra_imposter:
        item = dijkstra_imposter.get()
        cost, data = item.priority, item.data
        position, steps, direction = data

        if position == END_POSITON and steps >= min_step:
            return cost

        if steps >= min_step:
            for new_dir in (direction * 1j, direction * -1j):
                if next_cost := tiles.get(position + new_dir):
                    if is_best_heat(1, position + new_dir, cost + next_cost, new_dir):
                        dijkstra_imposter.put(PrioritizedItem(cost + next_cost, (position +new_dir, 1, new_dir)))

        if steps < max_step:
            if next_cost := tiles.get(position + direction):
                if is_best_heat(steps + 1, position + direction, cost + next_cost, direction):
                    dijkstra_imposter.put(PrioritizedItem(cost + next_cost, (position + direction, steps + 1, direction)))


print("Part 1: ", get_best_heat(1, 3))
print("Part 2: ", get_best_heat(4, 10))