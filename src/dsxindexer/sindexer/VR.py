from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class VR(BaseSindexer):
    """VR 成交量变异率
    计算公式：
    TH:=SUM(IF(CLOSE>REF(CLOSE,1),VOL,0),N);
    TL:=SUM(IF(CLOSE<REF(CLOSE,1),VOL,0),N);
    TQ:=SUM(IF(CLOSE=REF(CLOSE,1),VOL,0),N);
    VR:100*(TH*2+TQ)/(TL*2+TQ);
    MAVR:MA(VR,M);
    """
    __typename__ = "VR"

    def formula(self):
        return Formulas.VR()
    
    # 公式解析器会调用此方法
    def call(self,N=26,M=6):
        f = Formulas.VR(N,M)
        if f: return self.parser(f,self.__typename__)