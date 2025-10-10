import random

# 選択ソートアルゴリズム

random_val = [random.randint(1,100) for _ in range(10)]
print(random_val)


cnt:int = len(random_val)

for i in range(cnt):
    j:int = i + 1
    while j < cnt :
        
        if random_val[i] > random_val[j]:
            temp = random_val[i]
            random_val[i] = random_val[j]
            random_val[j] = temp
        # 内側の比較を１個進める
        j = j + 1  
        
    print(random_val)
             