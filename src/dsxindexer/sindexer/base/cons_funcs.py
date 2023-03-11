"""
常数函数(包括财务函数和动态行情函数)
"""
from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.base_sindexer import BaseSindexer

@property
def CAPITAL(self:BaseSindexer):
    """流通盘大小
    CAPITAL，返回流通盘大小，单位为手。
    对于A股得到流通A股，B股得到B股总股本，指数为0.注意：该函数返回常数
    例如：换手率公式：100*VOL/(CAPITAL);
    Args:
        self (BaseSindexer): _description_
    """

def FINANCE(self:BaseSindexer,N:int):
    """返回财务数据
    1=总股本        14=长期投资        27=上年损益调整
    2=国家股        15=流动负债        28=利润总额
    3=发起人法人股   16=长期负债        29=税后利润
    4=法人股        17=资本公积金      30=净利润
    5=B股          18=每股公积金      31=未分配利润
    6=H股          19=股东权益        32=每股未分配
    7=流通A股       20=主营收入        33=每股收益
    8=职工股        21=主营利润        34=每股净资产
    9=A2转配股      22=其他利润        35=调每股净资
    10=总资产       23=营业利润        36=股东权益比
    11=流动资产     24=投资收益        37=流通市值
    12=固定资产     25=补贴收入        38=总市值
    13=无形资产     26=营业外收支      39=上市日期
    Args:
        self (BaseSindexer): _description_
    """
   
def DYNAINFO(self:BaseSindexer,X:DSX_FIELD_STR):
    """动态行情函数
    3=昨收      16=委差         29=买二价       51=内外比
    4=今开      17=量比         30=买三价       52=多空平衡
    5=最高      18=            31=卖一量       53=多头获利
    6=最低      19=            32=卖二量       54=空头回补
    7=最新      20=委买价       33=卖三量       55=多头止损
    8=总手      21=委卖价       34=卖一价       56=空头止损
    9=现价      22=内盘         35=卖二价       57=笔升跌
    10=总额     23=外盘         36=卖三价
    11=均价     24=            37=换手率
    12=涨跌     25=买一量       38=5日均量
    13=振幅     26=买二量       39=市盈率
    14=涨幅     27=买三量       40=笔升跌
    15委比      28=买一价       50=采样点数
    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
    """