from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class PSY(BaseSindexer):
    """PSY 心理线
    计算方法：
        1.PSY=(N日内上涨天数/N)*100
        2.PSYMA=PSY的M日简单移动平均
        3.参数N设置为12日，参数M设置为6日
    """
    __typename__ = "PSY"
    
    def formula(self):
        return Formulas.PSY()
    
    # 公式解析器会调用此方法
    def call(self,N=12,M=6):
        f = Formulas.PSY(N,M)
        if f: return self.parser(f,self.__typename__)