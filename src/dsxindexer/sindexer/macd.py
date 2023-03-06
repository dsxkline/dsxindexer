from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class MACD(BaseSindexer):
    """MACD
    """
    __typename__ = "MACD"
    __exportvars__ = ("MACD","DIF","DEA")

    def formula(self):
        return Formulas.MACD()
    
    # 公式解析器会调用此方法
    def call(self,X,SHORT=12,LONG=26,MID=9,*args):
        f = Formulas.MACD(X,SHORT,LONG,MID)
        if f: return self.parser(f)