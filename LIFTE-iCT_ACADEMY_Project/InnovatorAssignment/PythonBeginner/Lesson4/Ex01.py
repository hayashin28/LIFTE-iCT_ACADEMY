# ループ回数をカウントするラムダ式の例

# ループ回数をカウントする関数
count_loops = lambda n: [i for i in range(n)]

# 例として10回ループする
loop_count = 10
result = count_loops(loop_count)

print(f"ループ回数: {len(result)}")
print(f"ループ結果: {result}")