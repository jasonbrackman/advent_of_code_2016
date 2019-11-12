#  MIT License
#
#  Copyright (c) 2019 Jason Brackman
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

from __future__ import annotations
import json
import time
from collections import deque
from heapq import heappop, heappush
from multiprocessing import Pool
from typing import Callable, Dict, Generic, List, Optional, TypeVar

T = TypeVar("T")


def get_lines(path: str) -> List[str]:
    with open(path, "r") as text:
        return [line.strip() for line in text.readlines()]


def load_json(path: str) -> dict:
    with open(path, "r") as o:

        return json.load(o)


def time_it(command):
    t1 = time.perf_counter()
    command()
    print(
        f"[{str(command.__module__)}.{command.__name__}: Completed in {time.perf_counter() - t1:0.8f} seconds"
    )


def time_it_all(args: List):
    with Pool(4) as p:
        p.map(time_it, args)


class Node:
    def __init__(self, state, parent):
        self.state = state
        self.parent = parent

    def __repr__(self):
        return f"Node({self.state!r}, {self.parent!r})"


def bfs(state, goal, successors):
    frontier = deque([Node(state, None)])
    visited = {hash(state)}

    count = 1
    while frontier:
        count += 1
        current_node = frontier.popleft()
        current_state = current_node.state

        if goal(current_state):
            # print(f"Processed {count} nodes.")
            return current_node

        for neighbor in successors(current_state):
            if hash(neighbor) in visited:
                continue
            visited.add(hash(neighbor))
            frontier.append(Node(neighbor, current_node))

    return None


def get_node_path_results(result, silent=True):
    flatten_nodes = list()
    if result is not None:
        flatten_nodes.append(result.state)
        while result.parent:
            result = result.parent
            flatten_nodes.append(result.state)
    for n in reversed(flatten_nodes):
        if not silent:
            print(n)

    return len(flatten_nodes)
