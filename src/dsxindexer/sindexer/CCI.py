from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class CCI(BaseSindexer):
    """CCI 顺势指标

    计算公式：
    以日CCI计算为例，其计算方法有两种。

    第一种计算过程如下：
        CCI（N日）=（TP－MA）÷MD÷0.015
        其中，TP=（最高价+最低价+收盘价）÷3
        MA=近N日收盘价的累计之和÷N
        MD=近N日（MA－收盘价）的绝对值的累计之和÷N
        0.015为计算系数，N为计算周期

    第二种计算方法表述为中价与中价的N日内移动平均的差除以0.015*N日内中价的平均绝对偏差
    其中，中价等于最高价、最低价和收盘价之和除以3
    平均绝对偏差为统计函数
    """
    __typename__ = "CCI"
    
    def formula(self):
        return Formulas.CCI()
    
    # 公式解析器会调用此方法
    def call(self,N=14):
        f = Formulas.CCI(N)
        if f: return self.parser(f,self.__typename__)