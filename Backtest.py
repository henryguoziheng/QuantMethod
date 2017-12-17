#coding:utf-8

import pandas as pd
import DataAPI as di

__author__ = 'Henry Guo'

def AccountUpdate():
    return

def UpdateAccount(mid_stock_account,mid_capital_account,stock_return):

    mid_stock_account['Trddt']=stock_return['Trddt'][0:1].values#更新日期
    mid_stock_account=pd.merge(mid_stock_account,stock_return)
    mid_stock_account['Price']=mid_stock_account['Clsprc']#更新当前持股价格
    mid_stock_account['MarketValue']=mid_stock_account['Amount']*mid_stock_account['Price']#当前持股每股市值
    mid_stock_account['Return']=(mid_stock_account['Price']-mid_stock_account['Buy_Price'])/mid_stock_account['Buy_Price']\
                                *mid_stock_account['Amount']#个股自买入的回报
    mid_stock_account=mid_stock_account[['Trddt','Stkcd','Amount','Buy_Price','Price','MarketValue','Return']]

    return mid_stock_account,mid_capital_account
"""
逐日回测框架
输入每个时间点股票组合（已处理过股票池），自动生成结果
过程：
1.进入第i日，检测是否调仓。
2.没有调仓，进入下一日；发生调仓，记录买卖股票名称，数量
调仓方式：今天10月1日，股票名单发生变化，我们假设今天开盘买入。
——剔除今天开盘不能交易股票，如：st，开盘涨停，开盘停牌。
3.生成今日个股收益，账户情况

记录：
总账户：日期，股票市值，现金市值，总市值
股票账户：日期，股票代码，持仓股数，买入价格，现价，持仓市值，损益||股票当日涨跌，仓内股票情况（停牌，行业*）
操作记录：日期，股票名称，操作，买入（卖出）价格，买入（卖出）股数，未成交的股票原因（0-正常，1-停牌，2-涨停）
买卖在开盘发生，三个账户记录收盘时情况。

（1）交易发生：以第一笔为例。
mid_stock_list不为空，调整mid_stock_list，变为应该持有的股数。
    调整mid_stock_list：读取当日股票交易数据。
    调出总市值账户昨日情况。
    剔除停牌，st，当日涨停的而股票。
    令权重*总市值/（当日开盘价*（1+trade_cost））的整100数，作为需买入股票股数。
生成当日的股票持仓，向股票账户添加记录。
核对新记录与上期股票持仓记录，生成当日操作记录。
核算今日总账户。
（2）没有交易：mid_stock_list为空，调整股票账户（添加新纪录）和总账户（股票市值变化，总市值变化）。
"""

begin_time='2014-06-01'#起始回测日期
end_time='2016-10-31'#结束回测日期
num=250#持仓股票数量
account=10000000#初始资金
trade_cost=0.05#交易成本，提高交易成本作为惩罚项

stock_list=pd.DataFrame(columns=['Trddt','Stkcd','Score'])#读入股票打分表，已删除st股票和上市未满6个月股票

capital_account=pd.DataFrame(columns=['Trddt','Portfolio_NetValue','Cash','Total_MarketValue'])#总账户
record={'Trddt':'start','Portfolio_NetValue':0,'Cash':account,'Total_MarketValue':account}#初始化账户
capital_account=pd.concat([capital_account,pd.DataFrame(record,index=[0])])
stock_account=pd.DataFrame(columns=['Trddt','Stkcd','Amount','Buy_Price','Price','MarketValue','Return'])#股票账户
trading_record=pd.DataFrame(columns=['Trddt','Stkcd','Buy/Sell','Price','Amount','Reason'])#操作账户

#回测时间轴
date_list=di.GetCalendar(begin_time,end_time)
date_list=date_list[date_list['State']=='O']
date_list=date_list[['Clddt']]
date_list.columns=['Trddt']

# stock_list=pd.merge(stock_list,date_list,how='outer')
# stock_list.fillna(method='pad',inplace=True)
# stock_list=stock_list[['Trddt','Stkcd','Score']]
# stock_list.sort_values(by=['Trddt','Score'])

for date in date_list['Trddt']:
    print date#输出回测日期



    stock_return=di.GetDalyTrd(TradeTime=date)#当日股票收益率
    # stock_return=stock_return[stock_return['Dnshrtrd']>0]#剔除停牌股票
    # stock_return=stock_return[stock_return['Dretnd']<0.098]#剔除涨停股票

    mid_stock_list=stock_list[stock_list['Trddt']==date]
    mid_stock_account,mid_capital_account=UpdateAccount(mid_stock_account,mid_capital_account,stock_return)

    stock_account=pd.concat([stock_account,mid_stock_account])
    capital_account=pd.concat([capital_account,mid_stock_account])