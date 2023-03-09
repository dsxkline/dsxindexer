from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer


class MA(BaseSindexer):
    """MA指标是英文(Moving average)的简写，叫移动平均线指标。
    1.N日MA=N日收市价的总和/N(即算术平均数)
    
    """
    __typename__ = "MA"

    # 公式解析器会调用此方法,这里自定义实现算法，通过公式实现就不用手动写算法了
    def call(self,X:DSX_FIELD_STR="CLOSE",N=5):
        amount = 0
        start = max(0,self.cursor.index - N)+1
        end = self.cursor.index+1
        M = 0
        for i in range(start,end):
            amount += self.GET(X,i)
            M += 1
        ma = M==0 and self.parser(X) or amount / M
        return ma