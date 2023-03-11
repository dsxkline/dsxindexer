"""
引用函数(MA、HHV、COUNT、REF、SUM、SMA等)
"""
from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.base_sindexer import BaseSindexer

def REF(self:BaseSindexer,X:DSX_FIELD_STR,N:int=1):
    """向前引用，向前引用必须跟公式MD5命名空间一致，否则多个调用之间会产生命名冲突
    """
    i = self.cursor.index - N
    if i<0:i=0
    if i>=0: 
        result = self.GET(X,i)
        if result==None:result=0
        return result

def LLV(self:BaseSindexer,X:DSX_FIELD_STR,N:int=1):
    """周期内最小值

    Args:
        X (str): 搜索的字段
        N (int, optional): _description_. Defaults to 1.
    """
    result = self.GET(X)
    index = self.cursor.index
    for i in range(N):
        index = self.cursor.index - i
        if index>=0:
            result = min(result,self.GET(X,index))
        else:
            break
    return result

def HHV(self:BaseSindexer,X:DSX_FIELD_STR,N:int=1):
    """周期内最大值

    Args:
        X (str): 搜索的字段
        N (int, optional): _description_. Defaults to 1.
    """
    result = self.GET(X)
    index = self.cursor.index
    for i in range(N):
        index = self.cursor.index - i
        if index>=0:
            result = max(result,self.GET(X,index))
        else:
            break
    return result

def HHVBARS(self:BaseSindexer,X:DSX_FIELD_STR, N=None):
    """上一高点位置求上一高点到当前的周期数。
    HHVBARS(X,N):求N周期内X最高值到当前周期数N=0表示从第一个有效值开始统计
    HHVBARS(HIGH,0)求得历史新高到到当前的周期数
    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
        N (_type_, optional): _description_. Defaults to None.
    """

def LLVBARS(self:BaseSindexer,X:DSX_FIELD_STR, N=None):
    """上一低点位置求上一低点到当前的周期数。
    LLVBARS(X,N):求N周期内X最低值到当前周期数N=0表示从第一个有效值开始统计
    LLVBARS(HIGH,20)求得20日最低点到当前的周期数
    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
        N (_type_, optional): _description_. Defaults to None.
    """


def REFDATE(self:BaseSindexer,X:DSX_FIELD_STR, N=None):
    """引用指定日期的数据
    例如：REFDATE(CLOSE, 1011208) 表示2011年12月08日的收盘价
    Args:
        X (DSX_FIELD_STR): _description_
        N (str): 日期 Ymd
    """
def BACKSET(self:BaseSindexer,X:DSX_FIELD_STR,N=1):
    """向前赋值，若X非0则把当前周期及前N－1周期的数值设置为1，属于未来函数
    例如: BACKSET(CLOSE>OPEN,2) 若收阳则将该周期及前一周期数值设为1,否则为0
    Args:
        X (DSX_FIELD_STR): _description_
        N (int, optional): _description_. Defaults to 1.
    """

def BARSCOUNT(self:BaseSindexer,X:DSX_FIELD_STR):
    """有效数据周期数
    第一个有效数据到当前的周期数
    例如 BARSCOUNT(CLOSE)
    对于日线，取得上市以来的周期数
    对于分笔成交，取得当日分笔成交笔数
    对于分钟线，取得当日交易分钟数

    Args:
        X (DSX_FIELD_STR): 字段
    """
    return self.klines.__len__()

def CURRBARSCOUNT(self:BaseSindexer,X:DSX_FIELD_STR):
    """到最后交易日的周期数
    
    Args:
        X (DSX_FIELD_STR): 字段
    """
def TOTALBARSCOUNT(self:BaseSindexer,X:DSX_FIELD_STR):
    """总的周期数
    
    Args:
        X (DSX_FIELD_STR): 字段
    """
def BARSLAST(self:BaseSindexer,X:DSX_FIELD_STR):
    """总的周期数
    BARSLAST(X):上一次X不为0到现在的天数
    BARSLAST(CLOSE/REF(CLOSE,1)>=1.1)表示上一个涨停板到当前的周期数
    Args:
        X (DSX_FIELD_STR): 字段
    """

def BARSSINCE(self:BaseSindexer,X:DSX_FIELD_STR):
    """第一个条件成立位置到当前的周期数。
    BARSSINCE(X):第一次X不为0到现在的天数。
    BARSSINCE(HIGH>10)表示股价超过10元时到当前的周期数
    Args:
        X (DSX_FIELD_STR): 字段
    """

def FILTER(self:BaseSindexer,X:DSX_FIELD_STR,N:int):
    """信号过滤过滤连续出现的信号。
    FILTER(X,N):X满足条件后，删除其后N周期内的数据置为0。
    FILTER(CLOSE>OPEN,5)查找阳线，5天内再次出现的阳线不被记录在内
    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
        N (float): _description_
    """

def SUMBARS(self:BaseSindexer,X:DSX_FIELD_STR,N:int):
    """累加到指定周期数向前累加到指定值到现在的周期数
    SUMBARS(X,A):将X向前累加直到大于等于A,返回这个区间的周期数
    SUMBARS(VOL,CAPITAL)求完全换手到现在的周期数

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
        N (int): _description_
    """