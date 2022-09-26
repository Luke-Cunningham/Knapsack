# Luke Cunningham
# Knapsack
import random
import time
import unittest
from hypothesis import given, assume
import hypothesis.strategies as st


def read_file(file_path):
    with open(file_path) as f:
        file_data = [tuple(map(int, line.split(' '))) for line in f]
    return file_data


def generate_inputs():
    items = []
    weight_capacity = 5000
    unique_count = 20
    for x in range(UNIQUE_COUNT):
        w = random.randint(1, 20)
        v = random.randint(1, 30)
        data.append((w, v))
    return weight_capacity, unique_count, items


def timer_func(func):
    def wrap_func(*args, **kwargs):
        runs = 3
        for run in range(runs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            if elapsed < 10:
                elapsed += elapsed / runs
            else:
                break
        print(f'Function {func.__name__!r} executed in {elapsed:.9f}s with result {result}')
        return result
    return wrap_func


@timer_func
def exhaustive_approach(weight_limit, item_count, items):
    power_set, power_set_values, power_set_indexes, knapsack_indexes = [], [], [], []
    highest_value = 0

    # Calculate powerset of item weights
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
    # Base Case
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
    return naive_recursion(weight_limit, item_count, items)


@timer_func
def dynamic_programming(weight_limit, item_count, items):
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


Item = st.dictionaries({'Weight': st.integers(min_value=1), 'Value': st.integers(min_value=1)})
ItemList = st.lists(Item)
Capacity = st.integers(min_value=1)


class TestSolution(unittest.TestCase):
    @given(Item, Capacity)
    def test_returns_a_fitting_result(self, weight_limit, item_count, items):
        result = dynamic_programming(weight_limit, item_count, items)
        self.assertLessEqual(
            sum(size for value, size in result),
            weight_limit
        )

# @given(ItemSet, Capacity)
# def test_returns_a_non_empty_result_if_any_fit(self, items, capacity):
#     assume(any(item[1] <= capacity for item in items))
#     result = solve_knapsack(items, capacity)
#     self.assertGreater(len(result), 0)
#
# @given(ItemSet, Capacity)
# def test_is_independent_of_order(self, items, capacity):
#     result = solve_knapsack(items, capacity)
#     items.reverse()
#     result2 = solve_knapsack(items, capacity)
#     self.assertEqual(score_solution(result), score_solution(result2))
#
# @given(ItemSet, Capacity, Capacity)
# def test_raising_capacity_cannot_worsen_solution(self, items, c1, c2):
#     assume(c1 != c2)
#     c1, c2 = sorted((c1, c2))
#     result1 = solve_knapsack(items, c1)
#     result2 = solve_knapsack(items, c2)
#     self.assertLessEqual(score_solution(result1), score_solution(result2))
#
# @given(ItemSet, Capacity)
# def test_increasing_score_of_chosen_item_improves_things(self, items, capacity):
#     assume(any(item[1] <= capacity for item in items))
#     result = solve_knapsack(items, capacity)
#     assert result
#     for item in result:
#         new_items = list(items)
#         new_items.append((item[0] + 1, item[1]))
#         new_result = solve_knapsack(new_items, capacity)
#         self.assertGreater(
#             score_solution(new_result),
#             score_solution(result))
#
# @given(ItemSet, Capacity)
# def test_increasing_weight_of_chosen_item_does_not_improve_things(self, items, capacity):
#     assume(any(item[1] <= capacity for item in items))
#     result = solve_knapsack(items, capacity)
#     assert result
#     for item in result:
#         new_items = list(items)
#         new_items.remove(item)
#         new_items.append((item[0], item[1] + 1))
#         new_result = solve_knapsack(new_items, capacity)
#         self.assertLessEqual(
#             score_solution(new_result), score_solution(result))
#
# @given(ItemSet, Capacity)
# def test_removing_a_chosen_item_does_not_improve_matters(self, items, capacity):
#     result = solve_knapsack(items, capacity)
#     score = score_solution(result)
#     for item in result:
#         new_items = list(items)
#         new_items.remove(item)
#         new_result = solve_knapsack(new_items, capacity)
#         self.assertLessEqual(score_solution(new_result), score)


if __name__ == '__main__':
    data = read_file("venv/Resources/Exhaustive_Verification")
    WEIGHT_CAPACITY, UNIQUE_COUNT = data.pop([0][0])[0], data.pop([0][0])[0]
    dict_list = []
    for d in range(UNIQUE_COUNT):
        current_dict = {'Weight': data[d][0], 'Value': data[d][1], 'Index': d + 1, 'Ratio': data[d][1] / data[d][0]}
        dict_list.append(current_dict)

    if UNIQUE_COUNT <= 22:
        exhaustive_approach(WEIGHT_CAPACITY, UNIQUE_COUNT, dict_list)
    heuristic_approach(WEIGHT_CAPACITY, dict_list)
    naive_recursion_timed(WEIGHT_CAPACITY, UNIQUE_COUNT, dict_list)
    dynamic_programming(WEIGHT_CAPACITY, UNIQUE_COUNT, dict_list)
