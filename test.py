#coding:utf-8

import pandas as pd
import DataAPI as di
import sys

__author__ = 'Henry Guo'

#reload(sys)
#sys.setdefaultencoding('utf-8')
stock_list=di.GetCoFunInfo()
#stock_list['Stknme']=stock_list['Stknme'].apply()
print stock_list['Stknme']