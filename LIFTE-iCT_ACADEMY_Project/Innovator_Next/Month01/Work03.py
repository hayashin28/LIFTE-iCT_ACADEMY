

# うるう年判定関数
def leap_year(year:int)-> bool:
    if (year % 400 == 0 or (year % 100 != 0 and year % 4 == 0)):
        return True
    else:
        return False


print('うるう年判定を行います')
print('4桁の数値を入力してください')
year = int(input())

# うるう年判定の結果を受け取る
truth_value = leap_year(year)
if (truth_value):
    print('うるう年です')
else:
    print('平年です')