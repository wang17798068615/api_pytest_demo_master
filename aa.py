s = "abcaaXY12ab12"
dict = {}

for i in range(0, len(s)):
    list = []  # 每次不记录dict字典中之前列表信息
  """
    # 想要每次记录dict中的value值，并往value值中新加数据，然后再进行dict替换，用setdefault函数

    dicts = {"a":["a,0"]}
    res = dicts.setdefault("a",[])
    print(res) # ['a,0']
    """
    list2 = dict.setdefault(s[i], [])  # 每次记录dict字典中之前列表信息
    print(list2)  # ['a ,0']
    list2.append(f"{s[i]} ,{i}") # ['a ,0', 'a ,3', 'a ,4']
    print(list2)  # ['a ,0', 'a ,3', 'a ,4']
    dict[s[i]] = list2  # ['a ,0'] = ['a ,0', 'a ,3', 'a ,4']

print(dict)  # {'a': ['a ,0', 'a ,3', 'a ,4', 'a ,9'], 'b': ['b ,1', 'b ,10'], 'c': ['c ,2'], 'X': ['X ,5'], 'Y': ['Y ,6'], '1': ['1 ,7', '1 ,11'], '2': ['2 ,8', '2 ,12']}

# 给定字符串，找出有重复的字符串，并输出其位置
# 输出格式: a, 1; a, 4; a, 5; a, 10; b, 2; b, 11; 1, 8; 1, 12; 2, 9; 2, 13


s = "abcaaXY12ab12"
from collections import Counter
data = {}
for index, char in enumerate(s):
    temp = data.setdefault(char, [])  # []
    temp.append('{}, {}'.format(char, index + 1))  # temp = ['a, 1']
    data[char] = temp  # data{a:['a, 1']}

print(data)  # {'a': ['a, 1']}
"""
{'a': ['a, 1', 'a, 4', 'a, 5', 'a, 10'], 'b': ['b, 2', 'b, 11'], 'c': ['c, 3'], 'X': ['X, 6'], 'Y': ['Y, 7'], '1': ['1, 8', '1, 12'], '2': ['2, 9', '2, 13']}
['a', 'b', '1', '2']
"""
list=[]
b = dict(Counter(s))
for key, value in b.items():
    if value > 1:
        list.extend(data[key])
print(list)  # ['a, 1', 'a, 4', 'a, 5', 'a, 10', 'b, 2', 'b, 11', '1, 8', '1, 12', '2, 9', '2, 13']
# 输出: a, 1; a, 4; a, 5; a, 10; b, 2; b, 11; 1, 8; 1, 12; 2, 9; 2, 13
str = "; "

str_res = str.join(res)
print(str_res)
"""
res = []
for value in data.values():
    if len(value) > 1:
        res.extend(value)
return '; '.join(res)
"""


