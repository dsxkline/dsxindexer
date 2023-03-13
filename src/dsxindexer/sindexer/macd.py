from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class MACD(BaseSindexer):
    """MACD
    """
    __typename__ = "MACD"

    def formula(self):
        return Formulas.MACD()
    
    # 公式解析器会调用此方法
    def call(self,X:DSX_FIELD_STR,SHORT=12,LONG=26,MID=9):
        f = Formulas.MACD(X,SHORT,LONG,MID)
        if f: return self.parser(f,self.__typename__)