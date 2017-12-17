#coding:utf-8

import pandas as pd
import DataAPI as di
import numpy as np
import datetime

__author__ = 'Henry Guo'


def UpdateTradeFactorCatch(begintime,endtime):
    print begintime
    stock_data=di.GetDalyTrd(BeginTime=begintime,EndTime=str(endtime)[0:10])
    ff=di.GetFF3F(BeginTime=begintime,EndTime=str(endtime)[0:10])
    stock_data=pd.merge(stock_data,ff)
    stock_data['c']=1
    i=0
    TradeFactor=pd.DataFrame()
    for code in stock_data['Stkcd'].unique():
        try:
            mid=stock_data[stock_data['Stkcd']==code]
            (x1,res,rank,s)=np.linalg.lstsq(mid[['MKT','c']],mid['Dretwd'])
            mid['e1']=mid['Dretwd']-np.dot(mid[['MKT','c']],x1)
            r1=1-res/((mid['Dretwd']-mid['Dretwd'].mean())*(mid['Dretwd']-mid['Dretwd'].mean())).sum()
            (x2,res,rank,s)=np.linalg.lstsq(mid[['MKT','SMB','HML','c']],mid['Dretwd'])
            mid['e2']=mid['Dretwd']-np.dot(mid[['MKT','SMB','HML','c']],x2)
            r2=1-res/((mid['Dretwd']-mid['Dretwd'].mean())*(mid['Dretwd']-mid['Dretwd'].mean())).sum()
            record=pd.DataFrame({'Trdmnt':str(endtime+pd.to_timedelta(5,'D'))[0:7],'Stkcd':code,'BetaCapm':x1[0],\
                                 'AlphaCapm':x1[1],'RCapm':r1,'StdECapm':mid['e1'].std(),'BetaMKT':x2[0],'BetaSMB':x2[1],\
                                 'BetaHML':x2[2],'RFF':r2,'StdEFF':mid['e2'].std(),'AlphaFF':x2[3]},index=[i])
        except:
            pass
        TradeFactor=pd.concat([TradeFactor,record])
        i+=1
    return TradeFactor

def UpdateTradeFactor():
    t=datetime.datetime.today()
    endtime=str(t)[0:4]+'-'+str(t)[5:7]+'-'+'01'
    begintime=t-pd.to_timedelta(10,'D')
    begintime=str(begintime)[0:4]+'-'+str(begintime)[5:7]+'-'+'01'
    data=UpdateTradeFactorCatch(begintime,endtime)
    data.to_excel(u'E:\\量化研究\\学术因子库\\TradeFactor\\%s.xls'%endtime,index=None)
    return

UpdateTradeFactor()