#coding:utf-8

import pandas as pd
import DataAPI as di
import numpy as np

__author__ = 'Henry Guo'

def CalMnt(date):
    """
    将时间处理为字符串
    :param date: 输入时间
    :return:时间字符串
    """
    date=str(date)[0:7]
    return date

def ClcExtrVal(data,col,d=5,u=95):
    """
    去除因子极值，默认为5%-95%。
    :param data: 输入的数据集
    :param col: 因子名称（即所在列）
    :param d: 下限
    :param u: 上限
    :return:因子序列
    """
    dl=np.percentile(data[col],d)
    ul=np.percentile(data[col],u)
    data=data[(data[col]>dl)&(data[col]<ul)]
    return data

def NormVal(data,col):
    """
    z-score标准化。
    :param data:数据集
    :param col: 因子名称（即所在列）
    :return:处理后数据集
    """
    data[col]=(data[col]-data[col].mean())/data[col].std()
    return data

def SetGroup(data,col,asd=True,n=10):
    """
    对于因子进行分组。
    :param data: 数据集。
    :param col: 因子名称（即所在列）
    :param asd: 递增排序or递减排序，默认为递增
    :param n: 分组组数
    :return:分组后的数据
    """
    data.sort_values(by=col,ascending=asd,inplace=True)
    #重新设定index
    data.index=range(len(data))
    data['Group']=0
    for i in range(n):
        if i==(n-1):
            data['Group'][(0+len(data)/n*i):len(data)]=i+1
        else:
            data['Group'][(0+len(data)/n*i):len(data)/n*(i+1)]=i+1
    return data

def FormFactorMnthReturn(BeginTime,EndTime,Factor_Name,Factor_Func,n=10,asd=True,StockPool='m',Benchmark=['zz500','equal']):
    """
    分组生成股票测试区间内每月的组合收益率。
    :param BeginTime: 测试起始时间YYYY-MM-DD。
    :param EndTime: 结束时间YYYY-MM-DD。
    :param Factor_Name: 因子名称（数据库中的列名）。
    :param Factor_Func: 提取该因子的di函数。
    :param n: 分组组数，默认为10组。
    :param asd:因子排序顺序，默认越高越差。
    :param Benchmark: 基准选择，默认为['zz500','equal']
    参数选择：上证50-sz50；沪深300-hs300；中证500-zz500；全市场,m，暂不能用。
    基准计算方式：指数-norm；等权-equal。
    :return:
    """
    print u'正在生成每组收益率……'
    #生成因子回测的时间序列
    date_list=pd.date_range(start=BeginTime,end=EndTime,freq='M')
    date_list=pd.DataFrame(date_list.tolist(),columns=['Trdmnt'])
    date_list['Trdmnt']=date_list['Trdmnt'].apply(CalMnt)

    GroupReturn=pd.DataFrame()#记录每月分组收益和对照组收益

    j=0

    for mnt in date_list['Trdmnt']:
        print mnt
        #读取因子数据
        factor=apply(Factor_Func,[mnt])

        #剔除st股票
        st_list=di.GetStList(TradeTime=mnt)#读取st列表
        factor=pd.merge(factor,st_list,how='outer')
        factor.fillna(1,inplace=True)
        factor=factor[factor['STflg']==1]

        #选择股票池
        if StockPool=='m':
            stock_pool=factor
        elif StockPool=='zz500':
            stock_pool=di.GetIndxCon(Indxcd='000905',TradeTime=mnt)
        elif StockPool=='sz50':
            stock_pool=di.GetIndxCon(Indxcd='000016',TradeTime=mnt)
        elif StockPool=='hs300':
            stock_pool=di.GetIndxCon(Indxcd='000300',TradeTime=mnt)

        #选择收益率基准
        if Benchmark[0]=='zz500':
            BenchmarkReturn=di.GetIndxTrm(TradeTime=mnt,IndexcdList=['000905'])
        elif Benchmark[0]=='sz50':
            BenchmarkReturn=di.GetIndxTrm(TradeTime=mnt,IndexcdList=['000016'])
        elif Benchmark[0]=='hs300':
            BenchmarkReturn=di.GetIndxTrm(TradeTime=mnt,IndexcdList=['000300'])

        factor=pd.merge(factor,stock_pool)
        factor=factor[['Stkcd','Trdmnt',Factor_Name]]
        BenchmarkReturn=BenchmarkReturn[['Trdmnt','Mretwd']]
        BenchmarkReturn.columns=['Trdmnt','IdxMretwd']

        #因子清洗
        factor=ClcExtrVal(factor,Factor_Name)#去极值
        factor=NormVal(factor,Factor_Name)#标准化
        factor=SetGroup(factor,Factor_Name,asd=asd,n=n)#股票分组

        #提取股票收益率
        stock_return=di.GetMnthTrd(TradeTime=mnt)
        stock_return=pd.merge(stock_return[['Trdmnt','Stkcd','Mretwd']],factor)

        #生成基准收益率
        if Benchmark[1]=='norm':
            stock_return=pd.merge(stock_return,BenchmarkReturn)
        else:
            stock_return['IdxMretwd']=stock_return['Mretwd'].mean()

        return_record={}
        for i in range(n):
            mid_return=stock_return[stock_return['Group']==(i+1)]
            return_record.update({u'日期':mnt,u'第%s组回报'%str(i+1):mid_return['Mretwd'].mean()})#记录各组合收益率

        return_record.update({u'基准回报':stock_return['IdxMretwd']})
        return_record=pd.DataFrame(return_record,index=[j])
        GroupReturn=pd.concat([GroupReturn,return_record])

    return GroupReturn

# 测试
# data=FormFactorGroupReturn(BeginTime='2010-06-01',EndTime='2016-09-30',n=10,Factor_Name='RFF',Factor_Func=di.GetTrdFactor,\
# Benchmark=['zz500','equal'])
# print data

def FormFactorGroupReturn(GroupReturn):
    """
    将每月各组收益率组合成资金净值曲线。
    :param GroupReturn: 每月每组组合收益率。
    :param save_loc: 储存地点，默认为None，不储存。
    :return:返回每组资金曲线。
    """
    print u'正在生成资金曲线……'

    col_list=[u'日期',u'基准回报']+[u'第%s组回报'%str(i) for i in range(1,11)]
    GroupReturn=GroupReturn[col_list]

    #计算胜率，每组波动率
    ProbRecord=pd.DataFrame()
    for i in range(10):
        win_prob=len(GroupReturn[GroupReturn[u'第%s组回报'%(str(i+1))]>GroupReturn[u'基准回报']])/float(len(GroupReturn))
        anual_std=GroupReturn[u'第%s组回报'%(str(i+1))].std()
        record={u'组别':str(i+1),u'月波动率':anual_std,u'胜率':win_prob}
        ProbRecord=pd.concat([ProbRecord,pd.DataFrame(record,index=[i])])

    #生成资金净值曲线
    for col in col_list[1:]:
        GroupReturn[col]=GroupReturn[col]+1
    strat_record=pd.DataFrame([['start']+[1]*11],columns=col_list)
    GroupReturn=pd.concat([strat_record,GroupReturn])
    for col in col_list[1:]:
        GroupReturn[col]=GroupReturn[col].cumprod()

    #计算每组年化收益率，基准年化收益率
    ReturnRecord=pd.DataFrame()
    for i in range(10):
        anual_return=pow(GroupReturn[u'第%s组回报'%(str(i+1))][len(GroupReturn)-1:len(GroupReturn)].tolist()[0],12./len(GroupReturn))-1
        record={u'组别':str(i+1),u'年化收益率':anual_return,u'基准回报':pow(GroupReturn[u'基准回报'][len(GroupReturn)-1:len(GroupReturn)].tolist()[0],12./len(GroupReturn))-1}
        ReturnRecord=pd.concat([ReturnRecord,pd.DataFrame(record,index=[i])])
    ReturnRecord=ReturnRecord[[u'组别',u'年化收益率',u'基准回报']]
    ReturnRecord=pd.merge(ProbRecord,ReturnRecord)

    return GroupReturn,ReturnRecord