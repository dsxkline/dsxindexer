"""
大盘函数(INDEXA、INDEXC、INDEXH等)
"""
from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.base_sindexer import BaseSindexer

@property
def INDEXA(self:BaseSindexer):
    """同期大盘成交额

    Args:
        self (BaseSindexer): _description_
    """
@property
def INDEXADV(self:BaseSindexer):
    """同期大盘的上涨家数

    Args:
        self (BaseSindexer): _description_
    """

@property
def INDEXC(self:BaseSindexer):
    """同期大盘收盘价

    Args:
        self (BaseSindexer): _description_

    """
@property
def INDEXDEC(self:BaseSindexer):
    """同期大盘下跌家数

    Args:
        self (BaseSindexer): _description_
    """
@property
def INDEXH(self:BaseSindexer):
    """同期大盘最高价

    Args:
        self (BaseSindexer): _description_
    """
@property
def INDEXL(self:BaseSindexer):
    """同期大盘最低价

    Args:
        self (BaseSindexer): _description_
    """
@property
def INDEXO(self:BaseSindexer):
    """同期大盘开盘价

    Args:
        self (BaseSindexer): _description_
    """
@property
def INDEXV(self:BaseSindexer):
    """同期大盘成交量

    Args:
        self (BaseSindexer): _description_
    """

