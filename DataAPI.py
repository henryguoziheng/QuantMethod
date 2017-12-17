#coding:utf-8

import pandas as pd
import MySQLdb as mdb

__author__ = 'Henry Guo'

"""

"""

"""
1.国泰安数据
"""
def GetCoFunInfo(StockList=None):
    """
    从CSMAR的trd_co表中获取上市公司基本信息，主要包括：行业，上市日期
    :param StockList:股票名称或者股票名称组
    :return:
    """
    con=mdb.connect('localhost', 'root','123456', 'csmar_stk_trd')
    cur=con.cursor()
    order="SELECT * from trd_co;"
    cur.execute(order)
    data = cur.fetchall()
    data=pd.DataFrame(list(data),columns=['Cuntrycd','Stkcd','Stknme','Conme','Conme_en','Indcd','Indnme','Nindcd','Nindnme',
                                          'Nnindcd','Nnindnme','Estbdt','Listdt','Favaldt','Curtrd','Ipoprm','Ipoprc','Ipocur',
                                          'Nshripo','Parvcur','Ipodt','Parval','Sctcd','Statco','Crcd','Statdt','Commnt','Markettype'])
    con.close()
    if StockList!=None:
        StockList=pd.DataFrame(StockList,columns=['Stkcd'])
        print StockList
        print data
        data=pd.merge(data,StockList)
    return data

def GetCalendar(BeginTime=None,EndTime=None):
    """
    从CSMAR的trd_cale表中获取日期列表
    :param BeginTime: 起始时间，若都为空，则选取整个列表
    :param EndTime: 结束时间，若都为空，则选取整个列表
    :return:
    """
    con=mdb.connect('localhost', 'root','19941123', 'csmar_stk_trd')
    cur=con.cursor()
    if (BeginTime==None)&(EndTime==None):
        order="SELECT * from trd_cale WHERE Markettype=1;"
    else:
        order="SELECT * from trd_cale WHERE (Markettype=1)&(Clddt>='%s')&(Clddt<='%s');"%(BeginTime,EndTime)
        print order
    cur.execute(order)
    data = cur.fetchall()
    data=pd.DataFrame(list(data),columns=['Markettype','Clddt','Daywk','State'])
    con.close()
    return data

def GetRfTrd(TradeTime=None,BeginTime=None,EndTime=None):
    """
    从CSMAR的trd_nrrate表中取得日度无风险利率，为定期-整存整取-一年利率
    :param TradeTime:如果只取一个日的数据，时间以YYYY-MM-DD形式传入
    :param BeginTime:起始时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :param EndTime:结束时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :return:
    """

    con=mdb.connect('localhost', 'root','19941123', 'csmar_stk_trd')
    cur=con.cursor()

    if TradeTime!=None:
        order="SELECT * from trd_nrrate WHERE Clsdt='%s'"%TradeTime
    elif (BeginTime!=None)&(EndTime!=None):
        order="SELECT * from trd_nrrate WHERE (Clsdt>='%s') & (Clsdt<='%s');"%(BeginTime,EndTime)
    else:
        data=None
    cur.execute(order)
    data = cur.fetchall()
    data=pd.DataFrame(list(data),columns=['Nrr1','Clsdt','Nrrdata','Nrrdaydt','Nrrwkdt','Nrrmtdt'])
    con.close()

    return data

def GetDalyTrd(Stkcd=None,TradeTime=None,BeginTime=None,EndTime=None,StockList=None):
    """
    从CSMAR的trd_dalyr表中取得日度交易数据
    :param TradeTime:如果只取一个日的数据，时间以YYYY-MM-DD形式传入
    :param BeginTime:起始时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :param EndTime:结束时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :param StockList:如果只取部分股票，以list形式传入
    :return:
    """
    con=mdb.connect('localhost', 'root','19941123', 'csmar_stk_trd')
    cur=con.cursor()

    if (TradeTime!=None)&(Stkcd!=None):
        order="SELECT * from trd_dalyr WHERE (Trddt='%s') & (Stkcd='%s');"%(TradeTime,Stkcd)
    elif (BeginTime!=None)&(EndTime!=None)&(Stkcd!=None):
        order="SELECT * from trd_dalyr WHERE (Trddt>='%s') & (Trddt<='%s') & (Stkcd='%s');"%(BeginTime,EndTime,Stkcd)
    elif (TradeTime!=None)&(Stkcd==None):
        order="SELECT * from trd_dalyr WHERE Trddt='%s';"%TradeTime
    elif (BeginTime!=None)&(EndTime!=None):
        order="SELECT * from trd_dalyr WHERE (Trddt>='%s') & (Trddt<='%s');"%(BeginTime,EndTime)
    else:
        data=None
    cur.execute(order)
    data = cur.fetchall()
    data=pd.DataFrame(list(data),columns=['Stkcd','Trddt','Opnprc','Hiprc','Loprc','Clsprc','Dnshrtrd','Dnvaltrd','Dsmvosd',
                                          'Dsmvtll','Dretwd','Dretnd','Adjprcwd','Adjprcnd','Markettype','Capchgdt','Trdsta'])
    con.close()

    if StockList!=None:
        StockList=pd.DataFrame(StockList,columns=['Stkcd'])
        data=pd.merge(data,StockList)

    return data

def GetMnthTrd(TradeTime=None,BeginTime=None,EndTime=None,StockList=None):
    """
    从CSMAR的trd_mnt表中取得月度交易数据
    :param TradeTime:如果只取一个月的数据，时间以YYYY-MM形式传入
    :param BeginTime:起始时间如果取一段时间的月数据，时间以YYYY-MM形式传入
    :param EndTime:结束时间如果取一段时间的月数据，时间以YYYY-MM形式传入
    :param StockList:如果只取部分股票，以list形式传入
    :return:
    """

    con=mdb.connect('localhost', 'root','19941123', 'csmar_stk_trd')
    cur=con.cursor()

    if TradeTime!=None:
        order="SELECT * from trd_mnth WHERE Trdmnt='%s'"%TradeTime
    elif (BeginTime!=None)&(EndTime!=None):
        order="SELECT * from trd_mnth WHERE Trdmnt>='%s' & Trdmnt<='%s';"%(BeginTime,EndTime)
    else:
        data=None
    cur.execute(order)
    data = cur.fetchall()
    data=pd.DataFrame(list(data),columns=['Stkcd','Trdmnt','Opndt','Mopnprc','Clsdt','Mclsprc','Mnshrtrd','Mnvaltrd','Msmvosd',
                                          'Msmvttl','Ndaytrd','Mretwd','Mretnd','Markettype','Capchgdt'])
    con.close()

    if StockList!=None:
        StockList=pd.DataFrame(StockList,columns=['Stkcd'])
        data=pd.merge(data,StockList)

    return data

"""
2.优矿数据
"""
def GetIndxCon(Indxcd='000300',TradeTime=None,BeginTime=None,EndTime=None):
    """
    从csmar_stk_trd的trd_indexcons表中取得沪深300指数000300，上证50指数000016，中证500指数000905名单
    :param Indxcd：沪深300指数000300，上证50指数000016，中证500指数000905，默认基准为沪深300
    :param TradeTime:如果只取一个日的数据，时间以YYYY-MM形式传入
    :param BeginTime:起始时间如果取一段时间的日数据，时间以YYYY-MM形式传入
    :param EndTime:结束时间如果取一段时间的日数据，时间以YYYY-MM形式传入
    :return:
    """

    con=mdb.connect('localhost', 'root','19941123', 'csmar_stk_trd')
    cur=con.cursor()

    if TradeTime!=None:
        order="SELECT * from trd_indexcons WHERE (Trdmnt='%s')&(Indexcd='%s')"%(TradeTime,Indxcd)
    elif (BeginTime!=None)&(EndTime!=None):
        order="SELECT * from trd_indexcons WHERE (Trdmnt>='%s') & (Trdmnt<='%s')&(Indexcd='%s');"%(BeginTime,EndTime,Indxcd)
    else:
        data=None
    cur.execute(order)
    data = cur.fetchall()
    data=pd.DataFrame(list(data),columns=['Indexcd','Stkcd','Trdmnt'])
    con.close()

    return data

def GetIndxTrd(TradeTime=None,BeginTime=None,EndTime=None,IndexcdList=None):
    """
    从CSMAR的trd_index_dalyr表中取得日度指数交易数据
    :param TradeTime:如果只取一个日的数据，时间以YYYY-MM-DD形式传入
    :param BeginTime:起始时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :param EndTime:结束时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :param IndexcdList:如果某个指数，以list形式传入
    :return:
    """
    con=mdb.connect('localhost', 'root','19941123', 'csmar_stk_trd')
    cur=con.cursor()

    if TradeTime!=None:
        order="SELECT * from trd_index_dalyr WHERE Trddt='%s'"%TradeTime
    elif (BeginTime!=None)&(EndTime!=None):
        order="SELECT * from trd_index_dalyr WHERE (Trddt>='%s') & (Trddt<='%s');"%(BeginTime,EndTime)
    else:
        data=None
    cur.execute(order)
    data = cur.fetchall()
    data=pd.DataFrame(list(data),columns=['Indexcd','Trddt','preClosePrice','Opnprc','Hiprc','Loprc','Clsprc','Dnshrtrd',
                                          'Dnvaltrd','chg','Mretwd'])
    con.close()

    if IndexcdList!=None:
        IndexcdList=pd.DataFrame(IndexcdList,columns=['Indexcd'])
        data=pd.merge(data,IndexcdList)

    return data

def GetIndxTrm(TradeTime=None,BeginTime=None,EndTime=None,IndexcdList=None):
    """
    从CSMAR的trd_index_mnth表中取得月度指数交易数据
    :param TradeTime:如果只取一个日的数据，时间以YYYY-MM形式传入
    :param BeginTime:起始时间如果取一段时间的日数据，时间以YYYY-MM形式传入
    :param EndTime:结束时间如果取一段时间的日数据，时间以YYYY-MM形式传入
    :param IndexcdList:如果某个指数，以list形式传入
    :return:
    """
    con=mdb.connect('localhost', 'root','19941123', 'csmar_stk_trd')
    cur=con.cursor()

    if TradeTime!=None:
        order="SELECT * from trd_index_mnth WHERE Trdmnt='%s'"%TradeTime
    elif (BeginTime!=None)&(EndTime!=None):
        order="SELECT * from trd_index_mnth WHERE (Trdmnt>='%s') & (Trdmnt<='%s');"%(BeginTime,EndTime)
    else:
        data=None
    cur.execute(order)
    data = cur.fetchall()
    data=pd.DataFrame(list(data),columns=['Indexcd','Clsdt','Ndaytrd','preClosePrice','Mopnprc','highestPrice',
                                          'lowestPrice','Mclsprc','Mnshrtrd','Mnvaltrd','chg','Mretwd','Trdmnt'])
    con.close()

    if IndexcdList!=None:
        IndexcdList=pd.DataFrame(IndexcdList,columns=['Indexcd'])
        data=pd.merge(data,IndexcdList)

    return data

def GetStList(TradeTime=None,BeginTime=None,EndTime=None):
    """
    从csmar_stk_trd的trd_st表中取得st股票名单
    :param TradeTime:如果只取一个日的数据，时间以YYYY-MM形式传入
    :param BeginTime:起始时间如果取一段时间的日数据，时间以YYYY-MM形式传入
    :param EndTime:结束时间如果取一段时间的日数据，时间以YYYY-MM形式传入
    :return:
    """

    con=mdb.connect('localhost', 'root','19941123', 'csmar_stk_trd')
    cur=con.cursor()

    if TradeTime!=None:
        order="SELECT * from trd_st WHERE Trdmnt='%s'"%TradeTime
    elif (BeginTime!=None)&(EndTime!=None):
        order="SELECT * from trd_st WHERE (Trdmnt>='%s') & (Trdmnt<='%s');"%(BeginTime,EndTime)
    else:
        data=None
    cur.execute(order)
    data = cur.fetchall()
    data=pd.DataFrame(list(data),columns=['Trdmnt','Stkcd','STflg'])
    con.close()

    return data

def GetFF3F(TradeTime=None,BeginTime=None,EndTime=None):
    """
    从alphafactor的ff3factor表中取得日度三因子SMB，HML，MKT
    :param TradeTime:如果只取一个日的数据，时间以YYYY-MM-DD形式传入
    :param BeginTime:起始时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :param EndTime:结束时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :return:
    """

    con=mdb.connect('localhost', 'root','19941123', 'alphafactor')
    cur=con.cursor()

    if TradeTime!=None:
        order="SELECT * from ff3factor WHERE Trddt='%s'"%TradeTime
    elif (BeginTime!=None)&(EndTime!=None):
        order="SELECT * from ff3factor WHERE (Trddt>='%s') & (Trddt<='%s');"%(BeginTime,EndTime)
    else:
        data=None
    cur.execute(order)
    data = cur.fetchall()
    data=pd.DataFrame(list(data),columns=['Trddt','SMB','HML','MKT'])
    con.close()

    return data

def Get3Factors(TradeTime=None,BeginTime=None,EndTime=None):
    """
    从alphafactor的3factors表中取得月度股票因子值LFLO，PE，PB
    :param TradeTime:如果只取一个日的数据，时间以YYYY-MM-DD形式传入
    :param BeginTime:起始时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :param EndTime:结束时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :return:
    """

    con=mdb.connect('localhost', 'root','19941123', 'alphafactor')
    cur=con.cursor()

    if TradeTime!=None:
        order="SELECT * from 3factors WHERE Trdmnt='%s'"%TradeTime
    elif (BeginTime!=None)&(EndTime!=None):
        order="SELECT * from 3factors WHERE (Trdmnt>='%s') & (Trdmnt<='%s');"%(BeginTime,EndTime)
    else:
        data=None
    cur.execute(order)
    data = cur.fetchall()
    data=pd.DataFrame(list(data),columns=['LFLO','PE','PB','Trdmnt','Stkcd'])
    con.close()
    return data

"""
3.学术因子
"""
def GetMarketValueFactor(TradeTime=None,BeginTime=None,EndTime=None):
    """
    从alphafactor的marketvaluefactor表中取得市值因子：Stkcd，Trdmnt，FMsmvttl，FMsmvosd，FLnMsmvttl，FLnMsmvosd
    :param TradeTime:如果只取一个日的数据，时间以YYYY-MM-DD形式传入
    :param BeginTime:起始时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :param EndTime:结束时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :return:
    """

    con=mdb.connect('localhost', 'root','19941123', 'alphafactor')
    cur=con.cursor()

    if TradeTime!=None:
        order="SELECT * from marketvaluefactor WHERE Trdmnt='%s'"%TradeTime
    elif (BeginTime!=None)&(EndTime!=None):
        order="SELECT * from marketvaluefactor WHERE (Trdmnt>='%s') & (Trdmnt<='%s');"%(BeginTime,EndTime)
    else:
        data=None
    cur.execute(order)
    data = cur.fetchall()
    data=pd.DataFrame(list(data),columns=['Stkcd','Trdmnt','FMsmvttl','FMsmvosd','FLnMsmvttl','FLnMsmvosd'])
    con.close()

    return data

def GetRetStatFactor(TradeTime=None,BeginTime=None,EndTime=None):
    """
    从alphafactor的retstatfactor表中取得市值因子：Stkcd,Trdmnt,FStd21,FStd63,FStd126,FStd252,FSkew21,FSkew63,FSkew126,FSkew252,FKurt21,FKurt63,FKurt126,FKurt252

    :param TradeTime:如果只取一个日的数据，时间以YYYY-MM-DD形式传入
    :param BeginTime:起始时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :param EndTime:结束时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :return:
    """

    con=mdb.connect('localhost', 'root','19941123', 'alphafactor')
    cur=con.cursor()

    if TradeTime!=None:
        order="SELECT * from retstatfactor WHERE Trdmnt='%s'"%TradeTime
    elif (BeginTime!=None)&(EndTime!=None):
        order="SELECT * from retstatfactor WHERE (Trdmnt>='%s') & (Trdmnt<='%s');"%(BeginTime,EndTime)
    else:
        data=None
    cur.execute(order)
    data = cur.fetchall()
    data=pd.DataFrame(list(data),columns=['Stkcd','Trdmnt','FStd21','FStd63','FStd126','FStd252','FSkew21','FSkew63',
                                          'FSkew126','FSkew252','FKurt21','FKurt63','FKurt126','FKurt252'])
    con.close()

    return data

def GetTrdFactor(TradeTime=None,BeginTime=None,EndTime=None):
    """
    从alphafactor的tradefactor表中取得月度交易因子：BetaCapm,AlphaCapm,RCapm,StdECapm,BetaMKT,BetaSMB,BetaHML,AlphaFF,RFF,StdFF
    :param TradeTime:如果只取一个日的数据，时间以YYYY-MM-DD形式传入
    :param BeginTime:起始时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :param EndTime:结束时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :return:
    """

    con=mdb.connect('localhost', 'root','19941123', 'alphafactor')
    cur=con.cursor()

    if TradeTime!=None:
        order="SELECT * from tradefactor WHERE Trdmnt='%s'"%TradeTime
    elif (BeginTime!=None)&(EndTime!=None):
        order="SELECT * from tradefactor WHERE (Trdmnt>='%s') & (Trdmnt<='%s');"%(BeginTime,EndTime)
    else:
        data=None
    cur.execute(order)
    data = cur.fetchall()
    data=pd.DataFrame(list(data),columns=['Trdmnt','Stkcd','BetaCapm','AlphaCapm','RCapm','StdECapm','BetaMKT','BetaSMB',
                                          'BetaHML','RFF','StdEFF','AlphaFF'])
    con.close()

    return data

def GetTurnoverFactor(TradeTime=None,BeginTime=None,EndTime=None):
    """
    从alphafactor的turnoverfactor表中取得月度交易因子：TO_MVFactor
    :param TradeTime:如果只取一个日的数据，时间以YYYY-MM-DD形式传入
    :param BeginTime:起始时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :param EndTime:结束时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :return:
    """

    con=mdb.connect('localhost', 'root','19941123', 'alphafactor')
    cur=con.cursor()

    if TradeTime!=None:
        order="SELECT * from turnoverfactor WHERE Trdmnt='%s'"%TradeTime
    elif (BeginTime!=None)&(EndTime!=None):
        order="SELECT * from turnoverfactor WHERE (Trdmnt>='%s') & (Trdmnt<='%s');"%(BeginTime,EndTime)
    else:
        data=None
    cur.execute(order)
    data = cur.fetchall()
    data=pd.DataFrame(list(data),columns=['Trdmnt','Stkcd','TO_MVFactor'])
    con.close()

    return data

def GetUtilityFactor(TradeTime=None,BeginTime=None,EndTime=None):
    """
    从alphafactor的utilityfactor表中取得月度交易因子：ClassicFactor
    :param TradeTime:如果只取一个日的数据，时间以YYYY-MM-DD形式传入
    :param BeginTime:起始时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :param EndTime:结束时间如果取一段时间的日数据，时间以YYYY-MM-DD形式传入
    :return:
    """

    con=mdb.connect('localhost', 'root','19941123', 'alphafactor')
    cur=con.cursor()

    if TradeTime!=None:
        order="SELECT * from utilityfactor WHERE Trdmnt='%s'"%TradeTime
    elif (BeginTime!=None)&(EndTime!=None):
        order="SELECT * from utilityfactor WHERE (Trdmnt>='%s') & (Trdmnt<='%s');"%(BeginTime,EndTime)
    else:
        data=None
    cur.execute(order)
    data = cur.fetchall()
    data=pd.DataFrame(list(data),columns=['Trdmnt','UtilityFactor','Stkcd'])
    con.close()

    return data