class Ex02:

    total:int = 0
    kamokus:list = ['国語', '数学', '理科', '社会', '英語']
    
    for kamoku in kamokus:
            
        while True:
            try:
                ten:int = int(input(f'{kamoku}の点数を入力してください：'))
                if (ten >= 0 and ten <= 100): 
                    total += ten
                    break
                else:
                    raise Exception

            except Exception as e: 
                print(f'不正な値を検知しました：{e}')       

    print(f'合計：{total}')