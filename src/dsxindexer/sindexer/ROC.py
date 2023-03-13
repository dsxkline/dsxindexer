from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class ROC(BaseSindexer):
    """ROC 变动率指标
    变动率指标（ROC），是以当日的收盘价和N天前的收盘价比较，通过计算股价某一段时间内收盘价变动的比例，应用价格的移动比较来测量价位动量，达到事先探测股价买卖供需力量的强弱，进而分析股价的趋势及其是否有转势的意愿，属于反趋势指标之一。
    计算公式：
    1.AX=今日收盘价-N日前收盘价
    2.BX=N日前收盘价
    3.ROC=AX/BX
    4.MAROC=ROC的M日移动平均线
    5.参数N为12参数M为6
    """
    __typename__ = "ROC"

    def formula(self):
        return Formulas.ROC()
    
    # 公式解析器会调用此方法
    def call(self,N=12,M=6):
        f = Formulas.ROC(N,M)
        if f: return self.parser(f,self.__typename__)