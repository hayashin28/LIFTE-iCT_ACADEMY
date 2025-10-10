# インデックスを指定してリストから要素を取り出す
spam = [
            ['cat', 'bat', 'rat', 'elephant'],
            [1, 2, 3, 4],
]

# インデックスを指定してリストから要素を取り出す
print(spam[0][3])  # 'elephant'
print(spam[1][3])  # 4  

#------ おうちミッション ------#
white:str = 'white'
black:str = 'black'

print(white)  # 'white' と出力
print(black)  # 'black' と出力

# 変数の中身を入れ替える
tmp = white
white = black
black = tmp
print(white)  # 'black' と出力
print(black)  # 'white' と出力
