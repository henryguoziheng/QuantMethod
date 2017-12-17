#coding:utf-8

import pandas as pd
import DataAPI as di
import datetime
import math
import numpy as np

__author__ = 'Henry Guo'


def UpdateTurnoverFactorCatch(month):
    l_month=str(pd.Timestamp(month)-pd.to_timedelta(1,'M'))[0:7]
    data=di.GetMnthTrd(TradeTime=l_month)

    data['LnTurnover']=data['Mnvaltrd']/data['Msmvosd']
    data['LnTurnover']=data['LnTurnover'].apply(math.log)#日对数换手率
    data['LnMsmvosd']=data['Msmvosd'].apply(math.log)#日对数流通市值
    data['c']=1

    (x1,res,rank,s)=np.linalg.lstsq(data[['LnMsmvosd','c']],data['LnTurnover'])#对数换手率对对数流通市值回归
    data['TO_MVFactor']=data['LnTurnover']-np.dot(data[['LnMsmvosd','c']],x1)
    data['Trdmnt']=month
    data=data[['Trdmnt','Stkcd','TO_MVFactor']]
    return data

def UpdateTurnoverFactor():
    t=datetime.datetime.today()
    month=str(t.year)+'-'+(2-len(str(t.month)))*'0'+str(t.month)
    data=UpdateTurnoverFactorCatch(month)
    data.to_excel(u'E:\\量化研究\\学术因子库\\TurnoverFactor\\%s.xls'%month,index=None)
    return

#test1
#data=UpdateTurnoverFactorCatch('2016-10')
#data.to_excel(u'E:\\量化研究\\学术因子库\\TurnoverFactor\\2016-10.xls',index=None)
UpdateTurnoverFactor()