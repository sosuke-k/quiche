import math
from sklearn.mixture import GMM

hoge = 10

def func(x):

    global hoge
    hoge = hoge + 1

    x.append('foo')
    x.append(hoge)
    return x