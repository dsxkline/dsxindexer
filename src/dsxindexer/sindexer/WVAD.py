from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class WVAD(BaseSindexer):
    """WVAD 威廉变异离散量
    计算公式：
    WVAD:SUM((CLOSE-OPEN)/(HIGH-LOW)*VOL,N)/10000;
    MAWVAD:MA(WVAD,M);
    """
    __typename__ = "WVAD"

    def formula(self):
        return Formulas.WVAD()
    
    # 公式解析器会调用此方法
    def call(self,N=24,M=6):
        f = Formulas.WVAD(N,M)
        if f: return self.parser(f,self.__typename__)