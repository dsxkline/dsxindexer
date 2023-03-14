from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class EMV(BaseSindexer):
    """EMV 简易波动指标
    如果较少的成交量就能推动股价上涨，则EMV数值会升高，相反的股价下跌时也仅伴随较少的成交量，则EMV数值将降低。另外，如价格不涨不跌，或者价格的上涨和下跌都伴随着较大的成交量时，则EMV的数值会趋近于零。
    计算公式：
    VOLUME:=MA(VOL,N)/VOL;
    MID:=100*(HIGH+LOW-REF(HIGH+LOW,1))/(HIGH+LOW);
    EMV:MA(MID*VOLUME*(HIGH-LOW)/MA(HIGH-LOW,N),N);
    MAEMV:MA(EMV,M);
    """
    __typename__ = "EMV"

    def formula(self):
        return Formulas.EMV()
    
    # 公式解析器会调用此方法
    def call(self,N=14,M=9):
        f = Formulas.EMV(N,M)
        if f: return self.parser(f,self.__typename__)