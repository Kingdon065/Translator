#! python3
# _*_ coding:utf-8 _*_

a = ['\n', '• asd','\n', 'hello']

with open('02.txt', 'a', encoding='utf-8') as f:
    f.writelines(a)