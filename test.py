__author__ = 'liuyin'
a = 9.999
b = round(a)
c = round(a,1)
d = int(a) + 1

i = 0
dictionary = {'a': 13, 'b': 14, 'c': 16}
for key in dictionary.keys():
    if key != 'a':
        i = i + 1

print i


