from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class KDJ(BaseSindexer):
    """KDJ指标
    RSV =(收盘价一N日内最低价的最低值)÷(N日内最高价的最高值-N日内最低价的最低值)x100
    K=RSV的M1日累积平均
    D=K的M2日累积平均
J=3×K-2×D
    """
    __typename__ = "KDJ"

    def formula(self):
        return Formulas.KDJ()
    
    # 公式解析器会调用此方法
    def call(self,X:DSX_FIELD_STR,N=9,M1=3,M2=3):
        f = Formulas.KDJ(X,N,M1,M2)
        if f: return self.parser(f,self.__typename__)