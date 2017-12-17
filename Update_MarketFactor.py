#coding:utf-8

import DataAPI as di
import pandas as pd
import math
import datetime

__author__ = 'Henry Guo'

def UpdateMarketFactorCatch(month):
    """
    跟新市值因子。
    :param month:当月月份
    :return:
    """
    l_month=str(pd.Timestamp(month)-pd.to_timedelta(1,'M'))[0:7]
    data=di.GetMnthTrd(TradeTime=l_month)
    data['Trdmnt']=month#滞后一月
    data['FMsmvttl']=data['Msmvttl']#总市值
    data['FMsmvosd']=data['Msmvosd']#流通市值
    data['FLnMsmvosd']=data['FMsmvosd'].apply(math.log)#对数流通市值
    data['FLnMsmvttl']=data['FMsmvttl'].apply(math.log)#对数总市值
    data=data[['Stkcd','Trdmnt','FMsmvttl','FMsmvosd','FLnMsmvttl','FLnMsmvosd']]
    return data

def UpdateMarketFactor():
    t=datetime.datetime.today()
    month=str(t.year)+'-'+(2-len(str(t.month)))*'0'+str(t.month)
    data=UpdateMarketFactorCatch(month)
    data.to_excel(u'E:\\量化研究\\学术因子库\\MarketValueFactor\\%s.xls'%month,index=None)
    return

#test1
#data=UpdateMarketFactorCatch('2016-10')
#data.to_excel(u'E:\\量化研究\\学术因子库\\MarketValueFactor\\2016-10.xls',index=None)

UpdateMarketFactor()