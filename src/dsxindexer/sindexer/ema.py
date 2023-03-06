from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer


class EMA(BaseSindexer):
    """EMA(Exponential Moving Average) 即指数移动平均线是一种常用的技术分析指标。
    EMA 的计算公式如下：
    EMA_t = (1-alpha)EMA_{t-1} + alpha C_t
    其中，C_t 是时间 t 的收盘价，EMA_t 是时间 t 的 EMA 值，alpha 是平滑因子，通常取 2/(N+1)，其中 N 为指定的时间周期。
    计算过程如下：
    计算第一个周期的EMA，即 EMA_1 = C_1。
    计算其他周期的EMA，对于第 t 个周期，先计算平滑因子 alpha$：alpha = 2/(N+1)。
    计算 EMA_t：EMA_t = (1-alpha)EMA_{t-1} + alpha C_t
    重复步骤 3 直到计算完所有周期的 EMA 值。
    需要注意的是，计算EMA的过程是一个递归过程，每个EMA的值依赖于前一个EMA的值。如果需要计算较长时间周期的EMA，可以使用指数平滑的方法，减小计算量。
    
    """
    __typename__ = "EMA"

    # 公式解析器会调用此方法,这里自定义实现算法，通过公式实现就不用手动写算法了
    def call(self,X,N,*args):
        XX = self.GET(X)
        alpha = 2/(N+1)
        last_key = X+"_EMA_"+str(N)
        if self.cursor.index==0 : 
            ema = XX
        else:
            last_ema = self.REF(last_key)
            ema = (1.0-alpha)*last_ema + alpha * XX
        self.save_temp(last_key,ema)
        return ema