"""
Luke Cunningham
Generating solutions for the NP-complete with exhaustive, heuristic, naive recursion, and dynamic programming
approaches.
"""
import math
import random
import time


def read_file(file_path):
    """
    Parse a txt file for the knapsack problem parameters and items.
    :param file_path: File to parse.
    :return: knapsack capacity, number of items to choose from, list of tuples (weight, value) for items
    """
    with open(file_path) as f:
        items = [tuple(map(int, line.split(' '))) for line in f]
    weight_limit, item_count = items.pop([0][0])[0], items.pop([0][0])[0]
    return weight_limit, item_count, items


def generate_inputs(weight_limit, item_count):
    """
    Randomly generate items' weights and values
    :param weight_limit: knapsack capacity
    :param item_count: number of items to choose from
    :return: knapsack capacity, number of items to choose from, list of tuples (weight, value) for items
    """
    items = []
    for _ in range(item_count):
        w = random.randint(1, math.ceil(weight_limit / 5))
        v = random.randint(1, math.ceil(weight_limit / 3))
        items.append((w, v))
    return weight_limit, item_count, items


def timer_func(func):
    """
    Wrapper function for timing method calls.
    :param func: function to time.
    :return: the result of the function.
    """
    def wrap_func(*args, **kwargs):
        elapsed, result = 0, 0
        runs = 3
        for run in range(runs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            if elapsed < 10:
                elapsed += elapsed / runs
            else:
                break
        print(f'Function {func.__name__!r} executed in {elapsed:.9f} seconds yielding a value of {result}')
        return result
    return wrap_func


@timer_func
def exhaustive_approach(weight_limit, item_count, items):
    """
    Generates the power set of item weights to calculate the subset with the highest cumulative value.
    :param weight_limit: knapsack capacity
    :param item_count: number of items to choose from
    :param items: list of tuples (weight, value)
    :return: the highest combination of item values possible
    """
    power_set, power_set_values, power_set_indexes, knapsack_indexes = [], [], [], []
    highest_value = 0

    # Generate power set of item weights
    for i in range(2 ** item_count):
        subset, subset_indexes = [], []
        subset_value = 0
        for j, item in enumerate(items):
            if i & 1 << j:
                subset.append(item.get('Weight'))
                subset_value += (item.get('Value'))
                subset_indexes.append((item.get('Index')))
        power_set.append(subset)
        power_set_values.append(subset_value)
        power_set_indexes.append(subset_indexes)

    # Calculate the highest value subset adhering to weight limit
    for subset_index, subset in enumerate(power_set):
        subset_value, subset_weight = 0, 0
        for item_index, item in enumerate(subset):
            subset_weight += item
            subset_value = power_set_values[subset_index]
        if subset_weight <= weight_limit and subset_value > highest_value:
            highest_value = subset_value
    return highest_value


@timer_func
def heuristic_approach(weight_limit, items):
    """
    heuristic approach prioritizes items with higher value per weight
    :param weight_limit: knapsack capacity
    :param items: list of tuples (weight, value)
    :return: combination of items (may not be optimal)
    """
    knapsack_indexes = []
    knapsack_value = 0
    current_weight = weight_limit

    # Sort by value descending then by ratio descending in accordance with tiebreak rule
    value_sorted_items = sorted(items, key=lambda item: item['Value'], reverse=True)
    ratio_sorted_items = sorted(value_sorted_items, key=lambda item: item['Ratio'], reverse=True)

    for itm in ratio_sorted_items:
        if itm.get('Weight') <= current_weight:
            knapsack_indexes.append(itm.get('Index'))
            knapsack_value += itm.get('Value')
            current_weight -= itm.get('Weight')
    return knapsack_value


def naive_recursion(weight_limit, item_count, items):
    """
    naive recursion approach
    :param weight_limit: knapsack capacity
    :param item_count: number of items to choose from
    :param items: list of tuples (weight, value)
    :return: the highest combination of item values possible
    """
    if weight_limit == 0 or item_count == 0:
        return 0

    # Ignore nth item if its weight is more than capacity
    if items[item_count - 1].get('Weight') > weight_limit:
        return naive_recursion(weight_limit, item_count - 1, items)

    else:
        return max(
            items[item_count - 1].get('Value') + naive_recursion(weight_limit - items[item_count - 1].get('Weight'),
                                                                 item_count - 1, items),
            naive_recursion(weight_limit, item_count - 1, items))


@timer_func
def naive_recursion_timed(weight_limit, item_count, items):
    """
    Naive recursive approach method call function. Provides wrapper functionality without unintended repeats.
    :param weight_limit: knapsack capacity
    :param item_count: number of items to choose from
    :param items: list of tuples (weight, value)
    :return: result of the naive_recursion method call
    """
    return naive_recursion(weight_limit, item_count, items)


@timer_func
def dynamic_programming(weight_limit, item_count, items):
    """
    "bottom up" dynamic programming approach
    :param weight_limit: knapsack capacity
    :param item_count: number of items to choose from
    :param items: list of tuples (weight, value)
    :return: the highest combination of item values possible
    """
    knapsack = [[0 for _ in range(weight_limit + 1)] for _ in range(item_count + 1)]

    # Build table knapsack[][] in bottom up manner
    for a in range(item_count + 1):
        for b in range(weight_limit + 1):
            if a == 0 or b == 0:
                knapsack[a][b] = 0
            elif items[a - 1].get('Weight') <= b:
                knapsack[a][b] = max(items[a - 1].get('Value') + knapsack[a - 1][b - items[a - 1].get('Weight')],
                                     knapsack[a - 1][b])
            else:
                knapsack[a][b] = knapsack[a - 1][b]
    return knapsack[item_count][weight_limit]


if __name__ == '__main__':
    # WEIGHT_CAPACITY, COUNT, data = read_file("venv/Resources/Exhaustive_Verification")
    WEIGHT_CAPACITY, COUNT, data = generate_inputs(500000, 21000)
    dict_list = []
    for d in range(COUNT):
        current_dict = {'Weight': data[d][0], 'Value': data[d][1], 'Index': d + 1, 'Ratio': data[d][1] / data[d][0]}
        dict_list.append(current_dict)

    heuristic_approach(WEIGHT_CAPACITY, dict_list)
    dynamic_programming(WEIGHT_CAPACITY, COUNT, dict_list)
    if COUNT <= 27:
        naive_recursion_timed(WEIGHT_CAPACITY, COUNT, dict_list)
    if COUNT <= 22:
        exhaustive_approach(WEIGHT_CAPACITY, COUNT, dict_list)
