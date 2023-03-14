from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class CR(BaseSindexer):
    """CR 带状能量线
    能量指标，即CR指标，CR指标又叫中间意愿指标、价格动量指标，它和AR、BR指标有很多相似之处，但更有自己独特的研判功能，是分析股市多空双方力量对比、把握买卖股票时机的一种中长期技术分析工具。
    计算公式：
    MID:=REF(HIGH+LOW,1)/2;
    CR:SUM(MAX(0,HIGH-MID),N)/SUM(MAX(0,MID-LOW),N)*100;
    MA1:REF(MA(CR,M1),M1/2.5+1);
    MA2:REF(MA(CR,M2),M2/2.5+1);
    MA3:REF(MA(CR,M3),M3/2.5+1);
    MA4:REF(MA(CR,M4),M4/2.5+1);
    """
    __typename__ = "CR"

    def formula(self):
        return Formulas.CR()
    
    # 公式解析器会调用此方法
    def call(self,N=26,M1=10,M2=20,M3=40,M4=62):
        f = Formulas.CR(N,M1,M2,M3,M4)
        if f: return self.parser(f,self.__typename__)