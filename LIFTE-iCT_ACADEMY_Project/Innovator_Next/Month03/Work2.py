import random

def digit(n:int)->str:
    # 一桁を判別する
    if n < 10:
        return str('  ' + str(n))
    # 二桁を判別する
    elif n < 100:
        return str(' ' + str(n))
    # 三桁が確定
    return str(n)
    
def matrix(rows, cols) ->list[list[int]]:

    # 値の範囲
    min_val, max_val = 1, 999
    # ランダムな値を持つ2次元配列を作る
    matrix = [
                [random.randint(min_val, max_val) for _ in range(cols)]
                    for _ in range(rows)]
    return matrix

mtx = matrix(5, 5)

#print('1～100までの値を入力して下さい:')
#n:int = int(input())

# 二次元配列の線形探索を行う
flg:bool = False    # 探索結果フラグ ※ breakはループ１個しかスキップできない
for c in range(len(mtx[0])):
    for r in range(len(mtx)):        
        if r == 4:
            # 改行付き出力
            print(digit(mtx[r][c]))
        else:
            # 改行無し出力
            print(digit(mtx[r][c]), end=',')
        

