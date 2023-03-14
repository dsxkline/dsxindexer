from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class DMA(BaseSindexer):
    """DMA 平均差
    平行线差（DMA）指标是利用两条不同期间的平均线，来判断当前买卖能量的大小和未来价格趋势。DMA指标是一种中短期指标。
    计算方法是
    DMA=股价短期平均值—股价长期平均值
    AMA=DMA短期平均值
    以求10日、50日为基准周期的DMA指标为例，其计算过程具体如下：
    DMA（10）=10日股价平均值—50日股价平均值
    AMA（10）=10日DMA平均值
    """
    __typename__ = "DMA"

    def formula(self):
        return Formulas.DMA()
    
    # 公式解析器会调用此方法
    def call(self,N1=10,N2=50,M=10):
        f = Formulas.DMA(N1,N2,M)
        if f: return self.parser(f,self.__typename__)