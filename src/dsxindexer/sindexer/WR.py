from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class WR(BaseSindexer):
    """WR 威廉指标
    W和R为测量行情振荡的指标，乃引用遇强则买，遇弱则卖的原理。
    计算公式：
    W%R=（Hn—C）÷（Hn—Ln）×100
    """
    __typename__ = "WR"

    def formula(self):
        return Formulas.WR()
    
    # 公式解析器会调用此方法
    def call(self,N=10,N1=6):
        f = Formulas.WR(N,N1)
        if f: return self.parser(f,self.__typename__)