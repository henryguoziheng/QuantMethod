#coding:utf-8

import DataAPI as di
import pandas as pd
import datetime

__author__ = 'Henry Guo'

def caldate(date):
    """
    将YYYY-MM-DD转为YYYY-MM。
    :param date: YYYY-MM-DD
    :return:YYYY-MM
    """
    date=str(date)[0:7]
    return date

def UpdateStdFactorsCatch(begintime,endtime):
    data=di.GetDalyTrd(BeginTime=begintime,EndTime=endtime)#读取数据
    print 'done'

    FactorData=pd.DataFrame()
    for code in data['Stkcd'].unique():
        print code
        mid=data[data['Stkcd']==code]
        for c in [21,63,126,252]:#前一个月,前一季度,前半年,前一年
            mid['FStd%s'%str(c)]=mid['Dretwd'].rolling(c).std()
            mid['FSkew%s'%str(c)]=mid['Dretwd'].rolling(c).skew()
            mid['FKurt%s'%str(c)]=mid['Dretwd'].rolling(c).kurt()

        mid.sort_values(by='Trddt',ascending=False,inplace=True)
        mid=mid[0:1]
        mid['Trdmnt']=str(endtime)[0:7]

        c=['FStd%s'%str(c) for c in [21,63,126,252]]
        c=c+['FSkew%s'%c for c in [21,63,126,252]]
        c=c+['FKurt%s'%c for c in [21,63,126,252]]
        FactorData=pd.concat([FactorData,mid[['Stkcd','Trdmnt']+c]])
        FactorData.dropna(inplace=True)
    return FactorData

def UpdateStdFactors():
    t=datetime.datetime.today()
    endtime=str(t)[0:4]+'-'+str(t)[5:7]+'-'+'01'
    begintime=endtime-pd.to_timedelta(400,'D')
    begintime=str(begintime)[0:10]
    data=UpdateStdFactorsCatch(begintime,endtime)
    data.to_excel(u'E:\\量化研究\\学术因子库\\StdFactor\\%s.xls'%endtime,index=None)
    return

UpdateStdFactors()
#data=UpdateStdFactorsCatch('2015-05-01','2016-10-01')
#data.to_excel(u'E:\\量化研究\\学术因子库\\StdFactor\\2016_10_01.xls',index=None)