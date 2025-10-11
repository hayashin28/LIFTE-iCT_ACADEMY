import random


while True:

    # ランダムな数値(1～100)を10個生成する
    random_val = [random.randint(1,100) for _ in range(10)]
    print(random_val)

    # リストの中からランダムな値を1つ取得する
    val = random.choice(random_val)

    #===== 選択ソートアルゴリズム =====#
    # 外側のループで小さい要素番号から確定する
    for i in range(len(random_val)):
        j = i + 1
        # 内側のループで、i + 1 番目～len(random_val)番目の値を比較し続ける
        while j < len(random_val):
            # 左辺の方が大きい場合は入れ替えが発生する
            if random_val[i] > random_val[j]:
                tmp = random_val[i]
                random_val[i] = random_val[j]
                random_val[j] = tmp
            # ループカウンターを1つ上げる
            j += 1

    # ソート結果を出力する
    print(random_val)


    # 二分探索
    # 探索範囲の最小値と最大値を設定する
    min:int = 0
    max:int = len(random_val) - 1   

    # 見つかったかどうかのフラグ
    flg:bool = False

    # 探索範囲がなくなるまで繰り返す
    while min <= max:    
        # 探索範囲の中央のインデックスを計算する
        # a / b は真の除算：常に少数(float)で返す
        # a // b は床除算：小数点以下を切り捨てて整数(int)で返す
        mid:int = (min + max) // 2

        print('正解と思う数値を入力してください（1～100）：')
        # input()はstr型で入るため、int型に変換する
        n:int = int(input())

        if val == n:
            print('正解！👺')
            flg = True
            break    
        # 中央の値と探索したい値を比較する
        #if random_val[mid] == val:
            #print(f'{n}は{mid}番目にあります。')
        #    print('正解！👺')
        #    flg = True
        #    break
        elif random_val[mid] < val:
            min = mid + 1
        else:
            max = mid - 1

        # ヒント出しを行う    
        if n < val:
            print(f'正解は{n}よりもっと大きい値です')
        else:
            print(f'正解は{n}よりもっと小さい値です')
        
        #====== ループの終わり ======#

    if flg == False:
        print(f'{n}は見つかりませんでした。')
        print(f'正解は{val}でした。')
    
    # もう一度挑戦するか確認
    print('もう一度挑戦しますか？(y/n)：')
    retry = input()
    
    if retry.lower() != 'y':
        break
