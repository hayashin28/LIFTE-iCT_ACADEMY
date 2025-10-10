import random

# バブルソートアルゴリズム

random_val = [random.randint(1,100) for _ in range(10)]
print(random_val)

for i in range(len(random_val)):
    for j in range(0, len(random_val) - i - 1):
        
        if random_val[j] > random_val[j + 1]:
            tmp = random_val[j]
            random_val[j] = random_val[j + 1]
            random_val[j + 1] = tmp

print(random_val)