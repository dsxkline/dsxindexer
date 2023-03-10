from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class BOLL(BaseSindexer):
    """
    BOLL线是一种常用的股票技术指标，它由三条线组成：中轨线、上轨线和下轨线。中轨线是一条移动平均线，上下轨线则是由中轨线加减标准差乘以系数得到的。
    BOLL线的计算公式如下：
    计算中轨线（MID）：
    MID = N日收盘价的累计和 ÷ N
    其中，N为计算周期，一般取20天。
    计算标准差（STD）：
    STD = √[∑(Ci - MID)² ÷ N]
    其中，Ci为收盘价，MB为中轨线，N为计算周期，一般取20天。
    计算上轨线（UP）：
    UP = MID + k × STD
    其中，k为系数，一般取2。
    计算下轨线（LOW）：
    LOW = MID - k × STD
    其中，k为系数，一般取2。
    以上就是BOLL线的计算公式。需要注意的是，不同的股票交易所和个股可能会有不同的计算周期和系数，所以在使用BOLL线指标时，需要根据实际情况进行调整。
    """
    __typename__ = "BOLL"
    
    def formula(self):
        return Formulas.BOLL()
    
    # 公式解析器会调用此方法
    def call(self,X:DSX_FIELD_STR,N=20,K=2):
        f = Formulas.BOLL(X,N,K)
        if f: return self.parser(f,self.__typename__)