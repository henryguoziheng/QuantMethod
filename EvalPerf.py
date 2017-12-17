# coding: utf-8
from __future__ import division
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

__author__ = 'Henry Guo'

"""
导入数据为：date,capital,benchmark

1.GetData(data)：规整数据columns和index

2.CalRtn(data)：计算股票收益率

3.AnnualReturn(data,freq='Mon',prt=True)：计算年化收益率，可以计算日频Day、月频Mon、分钟Min

4.MaxDrawdown(data,prt=True)：计算最大回撤比，最大回撤期，回撤期起始和结束日期

5.AverageChange(data,prt=True)：计算平均每日涨幅

6.ProbUp(data,prt=True)：计算上涨概率

7.ProbWin(data,prt=True)：计算组合胜率

8.Volatility(data,prt=True,freq='Day')：计算收益率波动率

9.Beta(data,prt=True)：计算beta

10.Alpha(data,prt=True,freq='Day')：计算alpha

11.SharpeRatio(data,prt=True,freq='Day')：计算夏普比率

12.InfoRatio(data,prt=True,freq='Day')：计算信息比率

13.CumulativeReturn(data,file_loc='',prt=False)：绘制收益率图像（与基准对比）
"""

def GetData(data):
    """
    规整数据行和列。
    :param data: 输入数据，属性顺序为日期、资金净值曲线、基准净值曲线。
    :return:规整后的数据colmuns为date,capital,benchmark。
    """
    f_data=data.copy()
    f_data.columns=['date','capital','benchmark']#重命名属性
    f_data.index=range(len(f_data))#重命名index
    return f_data

def CalRtn(data):
    """
    计算股票收益率。
    :param data: data为净值曲线，colmuns为date,capital，可能有benchmark
    :return:
    """
    f_data=GetData(data)#规整数据
    f_data['rtn']=(f_data['capital'].shift(0)-f_data['capital'].shift(1))/f_data['capital'].shift(1)

    if len(f_data.columns.tolist())==4:
        f_data['brtn']=(f_data['benchmark'].shift(0)-f_data['benchmark'].shift(1))/f_data['benchmark'].shift(1)

    return f_data

def AnnualReturn(data,freq='Mon',prt=True):
    """
    计算年化收益率，参考频率有：月，日，分钟
    :param data: 日期收益率序列，包含两列--日期，净值
    :return: 输出在回测期间的年化收益率
    """
    f_data=data.copy()
    f_data.columns=['date','capital']
    f_data.index=range(len(f_data))
    # 计算年化收益率
    if freq=='Mon':
        c=12.
    elif freq=='Day':
        c=252.
    elif freq=='Min':
        c=252*240.

    annual=pow(f_data.ix[len(f_data.index)-1,'capital']/f_data.ix[0,'capital'],c/len(f_data))-1

    if prt:
        print u'年化收益率为：%.2f' % (100*annual),'%'

    return annual

def MaxDrawdown(data,prt=True):
    """
    计算最大回撤，最大回撤期，起始日期，结束日期
    :param date_line: 日期收益率序列，包含两列--日期，净值
    :return: 输出最大回撤及开始日期和结束日期
    """
    f_data=GetData(data)#规整数据
    f_data['max2here']=pd.expanding_max(f_data['capital'])#计算当日之前的账户最大价值
    f_data['dd2here']=f_data['capital']/f_data['max2here']-1#计算当日的回撤

    # 计算最大回撤和结束时间
    temp=f_data.sort_values(by='dd2here').iloc[0][['date','dd2here']]
    max_dd=temp['dd2here'];end_date=temp['date']

    # 计算开始时间
    f_data=f_data[f_data['date']<=end_date]
    start_date=f_data.sort_values(by='capital', ascending=False).iloc[0]['date']
    if end_date=='start':
        end_date=start_date
    time=str(pd.Timestamp(end_date)-pd.Timestamp(start_date))

    if prt:
        print u'最大回撤为：%.2f%%, 最大回撤时间：%s ,开始日期：%s, 结束日期：%s' % (max_dd*100,time,start_date,end_date)

    return max_dd,time,start_date,end_date

def AverageChange(data,prt=True):
    """
    计算每日收益率的平均值
    :param date_line: 日期序列
    :param return_line: 账户日收益率序列
    :return: 输出平均涨幅
    """
    f_data=GetData(data)#规整数据
    f_data=CalRtn(f_data)
    ave=f_data['rtn'].mean()

    if prt:
        print u'平均涨幅为：%.2f' % (ave*100),'%'

    return ave

def ProbUp(data,prt=True):
    """
    计算上涨概率
    :param date_line: 日期序列
    :param return_line: 账户日收益率序列
    :return: 输出上涨概率
    """
    f_data=GetData(data)#规整数据
    f_data=CalRtn(f_data)
    f_data.ix[f_data['rtn']>0,'rtn']=1# 收益率大于0的记为1
    f_data.ix[f_data['rtn']<=0,'rtn']=0# 收益率小于等于0的记为0
    count=f_data['rtn'].value_counts()#统计1和0各出现的次数
    p_up=count.loc[1]/len(f_data.index)

    if prt:
        print u'上涨概率为：%.2f' % (p_up*100),'%'

    return p_up

def ProbWin(data,prt=True):
    """
    计算组合胜率。
    :param data: 原始数据
    :param prt: 是否打印
    :return:胜率
    """
    f_data=GetData(data)
    f_data=CalRtn(f_data)
    prob_win=len(f_data[f_data['rtn']>f_data['brtn']])/float(len(f_data))

    if prt==True:
        print u'胜率：%.2f'%(100*prob_win),'%'

    return prob_win

def Volatility(data,prt=True,freq='Day'):
    """
    计算收益波动率的函数
    :param date_line: 日期序列
    :param return_line: 账户日收益率序列
    :return: 输出回测期间的收益波动率
    """
    if freq=='Day':
        num=252
    else:
        num=12

    f_data=GetData(data)#规整数据
    f_data=CalRtn(f_data)
    from math import sqrt
    vol=f_data['rtn'].std()*sqrt(num)#计算波动率

    if prt:
        print u'收益波动率为：%.2f' % (vol*100),'%'

    return vol

def Beta(data,prt=True):
    """
    计算贝塔的函数
    :param date_line: 日期序列
    :param return_line: 账户日收益率序列
    :param indexreturn_line: 指数的收益率序列
    :return: 输出beta值
    """
    f_data=GetData(data)#规整数据
    f_data=CalRtn(f_data)
    b=f_data['rtn'].cov(f_data['brtn'])/f_data['brtn'].var()# 账户收益和基准收益的协方差除以基准收益的方差

    if prt:
        print 'beta: %.2f' % b

    return b

def Alpha(data,prt=True,freq='Day'):
    """
    计算alpha的函数
    :param date_line: 日期序列
    :param capital_line: 账户价值序列
    :param index_line: 指数序列
    :param return_line: 账户日收益率序列
    :param indexreturn_line: 指数的收益率序列
    :return: 输出alpha值
    """

    f_data=GetData(data)#规整数据
    f_data=CalRtn(f_data)

    rf = 0.0284#无风险利率取10年期国债的到期年化收益率
    annual_stock=AnnualReturn(f_data[['date','capital']],freq=freq,prt=False)# 账户年化收益
    annual_index=AnnualReturn(f_data[['date','benchmark']],freq=freq,prt=False)# 基准年化收益
    beta=f_data['rtn'].cov(f_data['brtn'])/f_data['brtn'].var()# 计算贝塔值
    a=(annual_stock-rf)-beta*(annual_index-rf)  # 计算alpha值

    if prt:
        print u'alpha：%.2f' % a

    return a

def SharpeRatio(data,prt=True,freq='Day'):
    """
    计算夏普比函数。
    :param date_line: 日期序列
    :param capital_line: 账户价值序列
    :param return_line: 账户日收益率序列
    :return: 输出夏普比率
    """
    if freq=='Day':
        num=252
    else:
        num=12

    f_data=GetData(data)#规整数据
    from math import sqrt
    f_data=CalRtn(f_data)
    rf = 0.0284  # 无风险利率取10年期国债的到期年化收益率
    annual_stock=AnnualReturn(f_data[['date','capital']],freq=freq,prt=False)# 账户年化收益
    volatility=f_data['rtn'].std()*sqrt(num)# 计算收益波动率
    sharpe=(annual_stock - rf)/volatility# 计算夏普比

    if prt:
        print 'sharpe_ratio: %.2f' % sharpe

    return sharpe

def InfoRatio(data,prt=True,freq='Day'):
    """
    粗略地计算信息比率函数。
    :param date_line: 日期序列
    :param return_line: 账户日收益率序列
    :param indexreturn_line: 指数的收益率序列
    :return: 输出信息比率
    """
    if freq=='Day':
        num=252
    else:
        num=12

    f_data=GetData(data)#规整数据
    from math import sqrt
    f_data=CalRtn(f_data)
    f_data['diff']=f_data['rtn']-f_data['brtn']
    annual_mean=f_data['diff'].mean()*num
    annual_std=f_data['diff'].std()*sqrt(num)
    info=annual_mean/annual_std

    if prt:
        print 'info_ratio: %.2f' % info

    return info

def CumulativeReturn(data,file_loc=None):
    """
    计算股票和基准在回测期间的累计收益率并画图，日级、月级都可。
    :param date_line: 日期序列
    :param return_line: 账户日收益率序列
    :param indexreturn_line: 指数日收益率序列
    :return: 画出股票和基准在回测期间的累计收益率的折线图
    """
    f_data=GetData(data)#规整数据
    f_data=CalRtn(f_data)

    # 画出股票和基准在回测期间的累计收益率的折线图
    fig=plt.figure()
    a0= fig.add_axes([0.09, 0.53, 0.89, 0.45])
    a1= fig.add_axes([0.09, 0.31, 0.89, 0.2])
    a2= fig.add_axes([0.09, 0.09, 0.89, 0.2])
    a0.plot(f_data['capital'],'ro-',label='Capital',linewidth=2,markerfacecolor='y', markersize=2)#组合累计收益率
    a0.plot(f_data['benchmark'],'bo-',label='Benchmark',linewidth=2,markerfacecolor='c', markersize=2)#基准收益率
    a0.set_xlim(-1,len(f_data))#横坐标数值设置
    a0.set_xticklabels([])#横坐标显示设置
    a0.legend(loc='best',fontsize='small')#图例设置
    a0.set_ylabel('Capital-Benchmark',fontsize='small')#纵坐标标题设置
    for t in a0.get_yticklabels():#纵坐标轴设置
        t.set_fontsize('x-small')

    #插入每月市场和组合收益率
    a1.bar(range(0,len(f_data)),f_data['brtn'],width=0.5,color='b',label='Benchmark')#沪深300每月收益率
    a1.bar([i-0.5 for i in range(0,len(f_data))],f_data['rtn'],width=0.5,color='r',label='AAR')#组合每月收益率
    a1.set_xlim(-1,len(f_data))#横坐标数值设置
    a1.set_xticklabels([])#横坐标范围设置
    a1.legend(loc='best',fontsize='small')#图例设置
    a1.set_ylabel('MonthlyRate',fontsize='small')#纵坐标标题设置
    for t in a1.get_yticklabels():#纵坐标轴设置
        t.set_fontsize('x-small')

    #插入每月组合收益率与沪深300收益率差额
    a2.bar(range(0,len(f_data)),(f_data['rtn']-f_data['brtn']),width=1,color='m',align='center',label='alpha')#每月组合收益率与沪深300收益率差额
    a2.set_xlim(-1,len(f_data))#横坐标数值设置
    a2.set_xticklabels([''],rotation=30,fontsize='xx-small')#横坐标范围设置
    a2.legend(loc='best',fontsize='small')#图例设置
    a2.set_ylabel('Alpha',fontsize='small')#纵坐标标题设置

    #纵坐标轴设置
    for t in a2.get_yticklabels():
        t.set_fontsize('x-small')

    #保存图像
    if file_loc!=None:
        plt.savefig(file_loc)

    #绘制图像
    plt.show()