#coding:utf-8

import pandas as pd
import EvalPerf as ep
import FormPFList as fl
import DataAPI as di
import os
import matplotlib.pyplot as plt

__author__ = 'Henry Guo'


def Assessment(data,name,save_file):
    """
    整理输出因子收益率。
    :param data: 原数据，包括日期、资金曲线，基准曲线三列。
    :param file_loc: 图像储存位置。
    :param name: 组合名称
    :return:
    """
    AR=ep.AnnualReturn(data[[u'日期',name]],freq='Mon',prt=True)
    max_dd,time,start_date,end_date=ep.MaxDrawdown(data,prt=True)
    AC=ep.AverageChange(data,prt=True)
    PU=ep.ProbUp(data)
    PW=ep.ProbWin(data)
    V=ep.Volatility(data,prt=True,freq='Mon')
    B=ep.Beta(data,prt=True)
    A=ep.Alpha(data,prt=True,freq='Mon')
    SR=ep.SharpeRatio(data,prt=True,freq='Mon')
    IR=ep.InfoRatio(data,prt=True,freq='Mon')
    ep.CumulativeReturn(data,file_loc=save_file)
    plt.close()
    record={ u'年化收益率':AR,u'最大回撤':max_dd,u'最大回撤时间':time,u'开始日期':start_date,u'结束日期':end_date,\
             u'平均涨幅':AC,u'上涨概率':PU,u'胜率':PW,u'收益波动率':V,'Beta':B,u'Alpha':A,'SharpeRatio':SR,\
             'InfoRatio':IR}
    record=pd.DataFrame(record,index=[name])
    return record

def FactorAssessment(BeginTime,EndTime,Factor_Name,Factor_Func,n=10,asd=True,StockPool='m',Benchmark=['zz500','equal'],file_loc=None):
    """
    评估因子收益。
    :param BeginTime:回测起始时间。
    :param EndTime: 回测结束时间。
    :param Factor_Name: 因子名称。
    :param Factor_Func: 提取因子函数。
    :param n: 分组数。
    :param asd: 因子升序or降序。
    :param stock_pool:回测股票池。
    :param Benchmark:基准。
    :param file_loc:文件夹位置。
    :return:
    """
    GroupReturn=fl.FormFactorMnthReturn(BeginTime,EndTime,Factor_Name,Factor_Func,n=n,asd=asd,StockPool=StockPool,Benchmark=Benchmark)
    ReturnData,ReturnRecord=fl.FormFactorGroupReturn(GroupReturn)
    print u'保存每月各组收益率结果……'
    ReturnData.plot(x=u'日期',y=[u'第%s组回报'%i for i in range(1,11)])
    plt.savefig(file_loc+u'每组净值曲线.png')
    plt.close()
    ReturnRecord=ReturnRecord[[u'组别',u'年化收益率',u'胜率',u'月波动率',u'基准回报']]
    ReturnRecord.to_excel(file_loc+u'分组收益率统计.xls',index=0)
    print u'输出保存分组组合……'
    ReturnRecord[[u'年化收益率',u'基准回报']].plot(kind='bar')
    plt.savefig(file_loc+u'分组组合结果.png')
    plt.close()

    #最好组表现
    print u'\n最优组表现：\n'
    data=ReturnData[[u'日期',u'第1组回报',u'基准回报']]
    record1=Assessment(data,u'第1组回报',file_loc+u'最优组表现.png')
    print u'\n最差组表现：\n'
    #最差组表现
    data=ReturnData[[u'日期',u'第10组回报',u'基准回报']]
    record2=Assessment(data,u'第10组回报',file_loc+u'最差组表现.png')

    #多空表现
    ReturnData[u'Top-Bottom多空组合']=ReturnData[u'第1组回报']-ReturnData[u'第10组回报']+1
    data=ReturnData[[u'日期',u'Top-Bottom多空组合',u'基准回报']]
    record3=Assessment(data,u'Top-Bottom多空组合',file_loc+u'Top-Bottom多空组表现.png')

    ReturnData[u'Top-Benchmark多空组合']=ReturnData[u'第1组回报']-ReturnData[u'基准回报']+1
    data=ReturnData[[u'日期',u'Top-Benchmark多空组合',u'基准回报']]
    record4=Assessment(data,u'Top-Benchmark多空组合',file_loc+u'Top-Benchmark多空组表现.png')

    print u'正在输出组合评价指标……'
    record=pd.DataFrame()
    record=pd.concat([record,record1])
    record=pd.concat([record,record2])
    record=pd.concat([record,record3])
    record=pd.concat([record,record4])
    record=record[[u'年化收益率',u'收益波动率',u'胜率',u'上涨概率',u'最大回撤',u'最大回撤时间',u'SharpeRatio',\
                   u'InfoRatio',u'开始日期',u'平均涨幅',u'结束日期',u'Alpha',u'Beta']]
    record.to_excel(file_loc+u'多空组合统计.xls')

    return

"""
1.拟合优度因子：全市场，等权中证500为基准
"""
FactorAssessment(BeginTime='2014-06-01',EndTime='2016-09-30',Factor_Name='RFF',Factor_Func=di.GetTrdFactor,n=10,asd=False,\
                 StockPool='m',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_拟合优度因子\\')
FactorAssessment(BeginTime='2010-06-01',EndTime='2014-06-01',Factor_Name='RFF',Factor_Func=di.GetTrdFactor,n=10,asd=False,\
                 StockPool='m',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_拟合优度因子\\')
#拟合优度因子：中证500，等权中证500为基准
FactorAssessment(BeginTime='2014-06-01',EndTime='2016-09-30',Factor_Name='RFF',Factor_Func=di.GetTrdFactor,n=10,asd=False,\
                  StockPool='zz500',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_拟合优度因子\\')
FactorAssessment(BeginTime='2010-06-01',EndTime='2014-06-01',Factor_Name='RFF',Factor_Func=di.GetTrdFactor,n=10,asd=False,\
                  StockPool='zz500',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_拟合优度因子\\')

"""
2.u'因子回测_残差标准差因子':全市场，等权中证500为基准
"""
#FactorAssessment(BeginTime='2014-06-01',EndTime='2016-09-30',Factor_Name='StdEFF',Factor_Func=di.GetTrdFactor,n=10,asd=True,\
#                 StockPool='m',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_残差标准差因子\\全市场_20140601_20160930\\')
#FactorAssessment(BeginTime='2010-06-01',EndTime='2014-06-01',Factor_Name='StdEFF',Factor_Func=di.GetTrdFactor,n=10,asd=True,\
#                 StockPool='m',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_残差标准差因子\\全市场_20100601_20140601\\')
#u'因子回测_残差标准差因子'中证500，等权中证500为基准
#FactorAssessment(BeginTime='2014-06-01',EndTime='2016-09-30',Factor_Name='StdEFF',Factor_Func=di.GetTrdFactor,n=10,asd=True,\
#                 StockPool='zz500',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_残差标准差因子\\中证500_20140601_20160930\\')
#FactorAssessment(BeginTime='2010-06-01',EndTime='2014-06-01',Factor_Name='StdEFF',Factor_Func=di.GetTrdFactor,n=10,asd=True,\
#                 StockPool='zz500',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_残差标准差因子\\中证500_20100601_20140601\\')

"""
3.因子回测：市值因子-对数流通市值，全市场+中证500
"""
#FactorAssessment(BeginTime='2014-06-01',EndTime='2016-09-30',Factor_Name='FLnMsmvosd',Factor_Func=di.GetMarketValueFactor,n=10,asd=True,\
#                 StockPool='m',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_市值因子\\对数流通市值_20140601_20160930_全市场\\')
#FactorAssessment(BeginTime='2014-06-01',EndTime='2016-09-30',Factor_Name='FLnMsmvosd',Factor_Func=di.GetMarketValueFactor,n=10,asd=True,\
#                 StockPool='zz500',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_市值因子\\对数流通市值_20140601_20160930_中证500\\')
#因子回测：市值因子-对数总市值，全市场+中证500
#FactorAssessment(BeginTime='2014-06-01',EndTime='2016-09-30',Factor_Name='FLnMsmvttl',Factor_Func=di.GetMarketValueFactor,n=10,asd=True,\
#                 StockPool='m',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_市值因子\\对数总市值_20140601_20160930_全市场\\')
#FactorAssessment(BeginTime='2014-06-01',EndTime='2016-09-30',Factor_Name='FLnMsmvttl',Factor_Func=di.GetMarketValueFactor,n=10,asd=True,\
#                 StockPool='zz500',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_市值因子\\对数总市值_20140601_20160930_中证500\\')

"""
4.偏度因子回测
"""
#for i in [21,63,126,252]:
#    p=u'E:\\量化研究\\学术因子库\\因子回测_偏度因子\\%s日偏度因子_20140601-20160930_全市场'%i
#    os.makedirs(p)
#    FactorAssessment(BeginTime='2014-06-01',EndTime='2016-09-30',Factor_Name='FSkew%s'%str(i),Factor_Func=di.GetRetStatFactor,n=10,asd=True,\
#                     StockPool='m',Benchmark=['zz500','equal'],file_loc=p+'\\')
#for i in [21,63,126,252]:
#    p=u'E:\\量化研究\\学术因子库\\因子回测_偏度因子\\%s日偏度因子_20140601-20160930_中证500'%i
#    os.makedirs(p)
#    FactorAssessment(BeginTime='2014-06-01',EndTime='2016-09-30',Factor_Name='FSkew%s'%str(i),Factor_Func=di.GetRetStatFactor,n=10,asd=True,\
#                     StockPool='zz500',Benchmark=['zz500','equal'],file_loc=p+'\\')

"""
5.PB因子回测
"""
#FactorAssessment(BeginTime='2014-06-01',EndTime='2016-09-30',Factor_Name='PB',Factor_Func=di.Get3Factors,n=10,asd=True,\
#                 StockPool='zz500',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_PB因子\\中证500_20140601_20160930\\')
#FactorAssessment(BeginTime='2010-06-01',EndTime='2014-06-01',Factor_Name='PB',Factor_Func=di.Get3Factors,n=10,asd=True,\
#                 StockPool='zz500',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_PB因子\\中证500_20100601_20140601\\')

"""
6.PE因子回测
"""
#FactorAssessment(BeginTime='2014-06-01',EndTime='2016-09-30',Factor_Name='PE',Factor_Func=di.Get3Factors,n=10,asd=True,\
#                 StockPool='zz500',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_PE因子\\中证500_20140601_20160930\\')
#FactorAssessment(BeginTime='2010-06-01',EndTime='2014-06-01',Factor_Name='PE',Factor_Func=di.Get3Factors,n=10,asd=True,\
#                 StockPool='zz500',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_PE因子\\中证500_20100601_20140601\\')

"""
7.换手率因子回测
"""
#FactorAssessment(BeginTime='2014-06-01',EndTime='2016-09-30',Factor_Name='TO_MVFactor',Factor_Func=di.GetTurnoverFactor,n=10,asd=True,\
#                 StockPool='zz500',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_换手率因子\\中证500_20140601_20160930\\')
#FactorAssessment(BeginTime='2010-06-01',EndTime='2014-06-01',Factor_Name='TO_MVFactor',Factor_Func=di.GetTurnoverFactor,n=10,asd=True,\
#                 StockPool='zz500',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_换手率因子\\中证500_20100601_20140601\\')

"""
8.效用因子
"""
#FactorAssessment(BeginTime='2014-06-01',EndTime='2016-09-30',Factor_Name='UtilityFactor',Factor_Func=di.GetUtilityFactor,n=10,asd=True,\
#                 StockPool='zz500',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_效用因子\\中证500_20140601_20160930\\')
#FactorAssessment(BeginTime='2010-06-01',EndTime='2014-06-01',Factor_Name='UtilityFactor',Factor_Func=di.GetUtilityFactor,n=10,asd=True,\
#                 StockPool='zz500',Benchmark=['zz500','equal'],file_loc=u'E:\\量化研究\\学术因子库\\因子回测_效用因子\\中证500_20100601_20140601\\')