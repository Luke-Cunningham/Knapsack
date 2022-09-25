# Luke Cunningham
# Knapsack
import random
import time
import unittest


def read_file(file_path):
    with open(file_path) as f:
        file_data = [tuple(map(int, line.split(' '))) for line in f]
    return file_data


def generate_inputs():
    data = []
    weight_capacity = 5000
    unique_count = 20
    for x in range(UNIQUE_COUNT):
        w = random.randint(1, 20)
        v = random.randint(1, 30)
        data.append((w, v))
    return weight_capacity, unique_count, data


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


# class TestSolution(unittest.TestCase):
#
#     def test_one(self):
#         self.assertEqual(solution("A", "K"), 1)


if __name__ == '__main__':
    RUN_COUNT = 3
    data = read_file("venv/Resources/Exhaustive_Verification")
    WEIGHT_CAPACITY, UNIQUE_COUNT = data.pop([0][0])[0], data.pop([0][0])[0]
    run_time, exhaustive_result, heuristic_result, naive_result, dynamic_result = 0, 0, 0, 0, 0


    dict_list = []
    for d in range(UNIQUE_COUNT):
        current_dict = {'Weight': data[d][0], 'Value': data[d][1], 'Index': d + 1, 'Ratio': data[d][1] / data[d][0]}
        dict_list.append(current_dict)

    approach_map = {
        'exhaustive': exhaustive_approach(WEIGHT_CAPACITY, UNIQUE_COUNT, dict_list),
        'heuristic': heuristic_approach(WEIGHT_CAPACITY, dict_list),
        'naive': naive_recursion(WEIGHT_CAPACITY, UNIQUE_COUNT, dict_list),
        'dynamic': dynamic_programming(WEIGHT_CAPACITY, UNIQUE_COUNT, dict_list)
    }

    for approach in approach_map:
        run_time = 0
        for run in range(RUN_COUNT):
            start = time.perf_counter()
            approach_result = approach_map[approach]
            end = time.perf_counter()
            run_time += ((end - start) / RUN_COUNT)
        print(f"The {approach} result is {approach_result} with a runtime of {run_time:.9f} seconds")

    # if UNIQUE_COUNT <= 22:
    #     for run in range(RUN_COUNT):
    #         start = time.perf_counter()
    #         exhaustive_result = approach_map.get('exhaustive')
    #         end = time.perf_counter()
    #         run_time += ((end - start) / RUN_COUNT)
    #     print(f"The exhaustive result is {exhaustive_result} with a runtime of {run_time:.9f} seconds")

    # run_time = 0
    # for run in range(RUN_COUNT):
    #     start = time.perf_counter()
    #     heuristic_result = heuristic_approach(WEIGHT_CAPACITY, dict_list)
    #     end = time.perf_counter()
    #     run_time += ((end - start) / RUN_COUNT)
    # print(f"The heuristic result is {heuristic_result} with a runtime of {run_time:.9f} seconds")
    #
    # run_time = 0
    # for run in range(RUN_COUNT):
    #     start = time.perf_counter()
    #     naive_result = naive_recursion(WEIGHT_CAPACITY, UNIQUE_COUNT, dict_list)
    #     end = time.perf_counter()
    #     run_time += ((end - start) / RUN_COUNT)
    # print(f"The naive recursive result is {naive_result} with a runtime of {run_time:.9f} seconds")
    #
    # run_time = 0
    # for run in range(RUN_COUNT):
    #     start = time.perf_counter()
    #     dynamic_result = dynamic_programming(WEIGHT_CAPACITY, UNIQUE_COUNT, dict_list)
    #     end = time.perf_counter()
    #     run_time += ((end - start) / RUN_COUNT)
    # print(f"The dynamic result is {dynamic_result} with a runtime of {run_time:.9f} seconds")
