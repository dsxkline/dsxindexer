from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class TRIX(BaseSindexer):
    """TRIX 三重指数平滑移动平均
    计算公式：
        1. TR=收盘价的N日指数移动平均；
        2.TRIX=(TR-昨日TR)/昨日TR*100；
        3.MATRIX=TRIX的M日简单移动平均；
        4.参数N设为12，参数M设为20；
        5.函数：TR := EMA(EMA(EMA(CLOSE,N),N),N);TRIX := (TR-REF(TR,1))/REF(TR,1)*100;TRMA := MA(TRIX,M)。
    """
    __typename__ = "TRIX"
    
    def formula(self):
        return Formulas.TRIX()
    
    # 公式解析器会调用此方法
    def call(self,X:DSX_FIELD_STR,N=12,M=9):
        f = Formulas.TRIX(X,N,M)
        if f: return self.parser(f,self.__typename__)