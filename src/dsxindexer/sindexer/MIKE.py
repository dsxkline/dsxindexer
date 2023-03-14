from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class MIKE(BaseSindexer):
    """MIKE 麦克支撑压力
    麦克支撑压力（MIKE）指标是一种股价波动幅度大小而变动的压力支撑指标，设有初级、中级、强力三种不同级别的支撑和压力，用图标方式直接显示压力、支撑的位置。
    计算公式：
    MID:=REF(HIGH+LOW,1)/2;
    CR:SUM(MAX(0,HIGH-MID),N)/SUM(MAX(0,MID-LOW),N)*100;
    MA1:REF(MA(CR,M1),M1/2.5+1);
    MA2:REF(MA(CR,M2),M2/2.5+1);
    MA3:REF(MA(CR,M3),M3/2.5+1);
    MA4:REF(MA(CR,M4),M4/2.5+1);
    """
    __typename__ = "MIKE"

    def formula(self):
        return Formulas.MIKE()
    
    # 公式解析器会调用此方法
    def call(self,N=10):
        f = Formulas.MIKE(N)
        if f: return self.parser(f,self.__typename__)