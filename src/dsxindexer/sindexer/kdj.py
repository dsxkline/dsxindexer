from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class KDJ(BaseSindexer):
    """KDJ指标
    """
    __typename__ = "KDJ"
    __exportvars__ = ("MACD2",)

    def formula(self):
        return Formulas.MACD2()
    
    # 公式解析器会调用此方法
    def call(self,X,SHORT=12,LONG=26,MID=9,*args):
        f = Formulas.MACD2(X,SHORT,LONG,MID)
        if f: return self.parser(f)