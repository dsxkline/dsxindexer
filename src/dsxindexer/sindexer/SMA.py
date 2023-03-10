from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer


class SMA(BaseSindexer):
    """SMA（Simple moving average(SMA)）简单移动平均线是一种最基础的技术指标。
    SMA 的计算公式如下：
    SMA(X,N,M) 求X的N日移动平均，M为权重。
    算法：
    若Y=SMA(X,N,M) 则 Y=(M*X+(N-M)*Y')/N，其中Y'表示上一周期Y值，N必须大于M。
    
    """
    __typename__ = "SMA"

    # 公式解析器会调用此方法,这里自定义实现算法，通过公式实现就不用手动写算法了
    def call(self,X:DSX_FIELD_STR,N,M):
        # if not isinstance(X,str):
        #     XX = X
        # else:
        XX = self.GET(X)
        # XX = self.GET(X)
        if N<=M: return
        last_key = "LY"+str(N)+str(X)
        LY = self.REF(last_key)
        if LY==None: LY = XX
        Y = (M*XX+(N-M)*LY)/N
        self.save_temp(last_key,Y)
        return Y