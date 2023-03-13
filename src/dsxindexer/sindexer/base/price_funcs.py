"""
行情函数(OPEN、CLOSE、HIGH、LOW、VOL等)
"""
from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.base_sindexer import BaseSindexer

@property
def OPEN(self:BaseSindexer):
    if self.klines:return self.klines[self.cursor.index].OPEN
@property
def HIGH(self:BaseSindexer):
    if self.klines:return self.klines[self.cursor.index].HIGH
@property
def LOW(self:BaseSindexer):
    if self.klines:return self.klines[self.cursor.index].LOW
@property
def CLOSE(self:BaseSindexer):
    if self.klines:return self.klines[self.cursor.index].CLOSE
@property
def VOL(self:BaseSindexer):
    if self.klines:return self.klines[self.cursor.index].VOL
@property
def AMOUNT(self:BaseSindexer):
    if self.klines:return self.klines[self.cursor.index].AMOUNT
@property
def DATE(self:BaseSindexer):
    if self.klines:return self.klines[self.cursor.index].DATE
@property
def O(self:BaseSindexer):
    if self.klines:return self.klines[self.cursor.index].OPEN
@property
def H(self:BaseSindexer):
    if self.klines:return self.klines[self.cursor.index].HIGH
@property
def L(self:BaseSindexer):
    if self.klines:return self.klines[self.cursor.index].LOW
@property
def C(self:BaseSindexer):
    if self.klines:return self.klines[self.cursor.index].CLOSE
@property
def V(self:BaseSindexer):
    if self.klines:return self.klines[self.cursor.index].VOL

@property
def ADVANCE(self:BaseSindexer):
    """返回该周期上涨家数 仅对大盘有效
    """
@property
def DECLINE(self:BaseSindexer):
    """返回该周期下跌家数 仅对大盘有效
    """
@property
def ASKPRICE(self:BaseSindexer,N=1):
    """委卖价

    Args:
        N (int, optional): _description_. Defaults to 1.
    """
@property
def ASKVOL(self:BaseSindexer,N=1):
    """委卖量

    Args:
        N (int, optional): _description_. Defaults to 1.
    """
@property
def BIDPRICE(self:BaseSindexer,N=1):
    """委买价

    Args:
        N (int, optional): _description_. Defaults to 1.
    """
@property
def BIDVOL(self:BaseSindexer,N=1):
    """委买量

    Args:
        N (int, optional): _description_. Defaults to 1.
    """
@property
def BUYVOL(self:BaseSindexer):
    """主动性买单量
    当本笔成交为主动性买盘时，其数值等于成交量，否则为0。（本函数仅在个股分笔成交分析周期有效）
    """
@property
def SELLVOL(self:BaseSindexer):
    """主动性卖单量
    当本笔成交为主动性卖盘时，其数值等于成交量，否则为0。（本函数仅在个股分笔成交分析周期有效）
    """
@property
def ISBUYORDER(self:BaseSindexer):
    """是否主动性买单
    当本笔成交为主动性买盘时，其数值等于1，否则为0。（本函数仅在个股分笔成交分析周期有效）
    """
@property
def ISSELLORDER(self:BaseSindexer):
    """是否主动性卖单
    当本笔成交为主动性卖盘时，其数值等于1，否则为0。（本函数仅在个股分笔成交分析周期有效）
    """