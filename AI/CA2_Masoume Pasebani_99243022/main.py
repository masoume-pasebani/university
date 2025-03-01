import random
import numpy as np
def binary_random():
    result = [None]
    for i in range(100):
        rand = random.randint(0, 1)
        result.append(rand)
    return result
def is_key(binary_num, input):
    for item in input:
        if (item[0] > 0 and binary_num[item[0]] == 1) \
                or (item[1] > 0 and binary_num[item[1]] == 1) \
                or (item[2] > 0 and binary_num[item[2]] == 1) \
                or (item[0] < 0 and binary_num[-item[0]] == 0) \
                or (item[1] < 0 and binary_num[-item[1]] == 0) \
                or (item[2] < 0 and binary_num[-item[2]] == 0):
            pass
        else:
            return False
    return True
def high_rate(binary_num, input):
    nums_true = 0
    for item in input:
        if (item[0] > 0 and binary_num[item[0]] == 1) \
                or (item[1] > 0 and binary_num[item[1]] == 1) \
                or (item[2] > 0 and binary_num[item[2]] == 1) \
                or (item[0] < 0 and binary_num[-item[0]] == 0) \
                or (item[1] < 0 and binary_num[-item[1]] == 0) \
                or (item[2] < 0 and binary_num[-item[2]] == 0):
            nums_true += 1

    return nums_true
def sort(binary_num, input):
    score_list = []
    for num in binary_num:
        score_list.append((high_rate(num, input), num))
    score_list.sort(key=lambda x: x[0])
    return score_list
def genetic(random_numbers, input):
    for i in range(1000):
        random_numbers = map(lambda tp: tp[1], sort(random_numbers, input))
        random_numbers = list(random_numbers)
        bad_genes = random_numbers[0:10]
        good_genes = random_numbers[40:50]
        good_rand = random.randint(0, 9)
        bad_rand = random.randint(0, 9)
        random_numbers = crossover(random_numbers, good_genes[good_rand], bad_genes[bad_rand])
    return random_numbers
def crossover(generated_num, parent1, parent2):
    rand = random.randint(0, 99)
    child1 = []
    child2 = []
    child1.append(None)
    child2.append(None)
    child1 += parent1[0:rand] + parent2[rand:101]
    child2 += parent2[0:rand] + parent1[rand:101]
    generated_num.append(child1)
    generated_num.append(child2)
    generated_num.remove(parent1)
    generated_num.remove(parent2)
    return generated_num


lines = np.genfromtxt("input.cnf", dtype=int, delimiter="  ", unpack=False)
temp = ""
input = [[] for i in range(0, 429)]

# to access each variable use this line :
col = 0
binary_rand_number = [binary_random() for _ in range(50)]
for i in np.nditer(lines):
    if i == 0:
        col += 1
    else:
        input[col].append(int(i))

binary_rand_number = genetic(binary_rand_number, input)

num = 0
for i in binary_rand_number:
    if is_key(i, input):
        num += 1
        print(f'The {num}th key: {" ".join(str(e) for e in i)}')
