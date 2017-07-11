# coding=utf-8
import codecs

from Portfolio_Formation import *

path = u'Z:\Mac 上的 WangBin-Mac\FOF\Robo-Advisor'

for each in range(1,11):
    portfolio_imformation = Portfolio_Form(each)
    full_path = path + "\portfolio_" + str(each) + '.txt'
    file = codecs.open(full_path, 'w', 'utf-8')
    file.write(portfolio_imformation)
    file.close()
    print('Done')

for each in range(1, 11):
    full_path = path + "\portfolio_" + str(each) + '.txt'
    file = codecs.open(full_path)
    print file.read()

full_path = '/Users/WangBin-Mac/FOF/Robo-Advisor/portfolio_1.txt'
