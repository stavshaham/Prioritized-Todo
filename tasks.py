# tasks.py - by Stav Shaham
# This file manages tasks using a min-heap priority queue.

import heapq
import itertools
import file_handler as fh

# Each heap item has this structure:
#
# (priority, order, task)
#
# The heap compares priority first.
# Therefore:
# 1 = High
# 2 = Medium
# 3 = Low
#
# The order value is used when two tasks have the same priority.
task_queue = []

# Generates a unique order number for each task.
task_counter = itertools.count()

def add_task(name, priority):
    """
    Add a task to the priority queue.

    Time complexity:
        heapq.heappush() takes O(log n) because the new item
        may move upward through the height of the heap.

        save_tasks() takes O(n log n) because it removes every
        item from a copied heap using heappop(). Each heappop()
        takes O(log n).

        Overall complexity: O(n log n)
    """

    task = {
        "name": name,
        "priority": priority,
        "done": False
    }

    # Give the task a unique order number.
    order = next(task_counter)

    # Add the task to the heap.
    # heappush() places the item at the end and heapify
    heapq.heappush(
        task_queue,
        (priority, order, task)
    )

    save_tasks()


def view_tasks():
    """
    Return all tasks in priority order.

    Time complexity:
        Copying the heap takes O(n).

        The while loop runs n times because every task is
        removed from the copied heap once.

        Each heappop() takes O(log n), because the replacement
        item may move down through the height of the heap.

        n removals multiplied by O(log n) gives O(n log n).

        Overall complexity: O(n log n)
    """

    # Copy the heap so the actual task_queue is not destroyed.
    #
    # If we popped directly from task_queue, all tasks would be
    # removed from the application's actual priority queue.
    temporary_queue = task_queue.copy()

    ordered_tasks = []

    # Remove the smallest item repeatedly.
    # The smallest priority number represents the most important task.
    while len(temporary_queue) > 0:
        # heappop() removes the root of the min-heap, then heapify again.
        priority, order, task = heapq.heappop(
            temporary_queue
        )

        # Store only the task dictionary.
        ordered_tasks.append(task)

    return ordered_tasks


def mark_done(task, completed):
    """
    Mark a task as completed or incomplete.

    Time complexity:
        Changing the dictionary value takes O(1).

        However, save_tasks() takes O(n log n), because it
        removes all tasks from a copied heap to save them
        in priority order.

        Overall complexity: O(n log n)
    """

    # Dictionary access and modification take constant time.
    task["done"] = completed
    save_tasks()


def remove_completed_tasks():
    """
    Remove all completed tasks.

    Time complexity:
        The for loop checks every task once: O(n).

        heapq.heapify() rebuilds the heap in O(n) time.

        save_tasks() takes O(n log n), because it uses repeated
        heappop() operations to save tasks in priority order.

        Overall complexity: O(n log n)
    """

    global task_queue

    remaining_tasks = []

    # Visit every item once.
    for item in task_queue:
        # The task dictionary is the third part of the tuple.
        task = item[2]
        # Keep only unfinished tasks.
        if not task["done"]:
            remaining_tasks.append(item)

    # Replace the old queue.
    task_queue = remaining_tasks

    # heapify() is O(n)
    heapq.heapify(task_queue)

    save_tasks()


def save_tasks():
    """
    Save all tasks to data.json.

    Time complexity:
        view_tasks() takes O(n log n), because it repeatedly
        removes tasks from a copied heap.

        Writing n tasks to the JSON file takes O(n).

        O(n log n) dominates O(n).

        Overall complexity: O(n log n)
    """

    # Get the tasks in priority order.
    data = view_tasks()
    fh.save_data(data)


def load_data_from_file():
    """
    Load tasks from data.json.

    Time complexity:
        Reading n tasks from the file takes O(n).

        Adding all tasks to a regular list takes O(n).

        heapq.heapify() converts the complete list into a heap
        in O(n) time.

        Overall complexity: O(n)
    """

    global task_queue
    # Start with an empty queue.
    task_queue = []
    # Read the saved task dictionaries.
    data = fh.load_data()

    # Add every saved task to a regular list.
    for task in data:
        # Give old tasks default values.
        task.setdefault("priority", 2)
        task.setdefault("done", False)

        # Give the task a unique order number.
        order = next(task_counter)

        # Add the tuple to the list.
        task_queue.append(
            (task["priority"], order, task)
        )

    # heapify() is O(n)
    heapq.heapify(task_queue)