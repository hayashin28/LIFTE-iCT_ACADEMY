class Ex03:
    
    user1:set = [None] * 5
    user2:set = [None] * 5

    i:int = 0
    for i in range(len(user1)):
        user1[i] = input(f'user1の{i + 1}番目の趣味を入力してください：')

    i:int = 0        
    for i in range(len(user2)):
        user2[i] = input(f'user2の{i + 1}番目の趣味を入力してください：')
    
    
    print(f'2人の相性は{len(set(user1) & set(user2)) / len(set(user1) | set(user2)) * 100}でした')