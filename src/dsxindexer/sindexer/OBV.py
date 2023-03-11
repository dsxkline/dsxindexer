from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class OBV(BaseSindexer):
    """OBV 累积能量线 能量潮指标（On Balance Volume，OBV）
    计算方法：
        以某日为基期，逐日累计每日上市股票总成交量，若隔日指数或股票上涨，则基期OBV加上本日成交量为本日OBV。隔日指数或股票下跌，则基期OBV减去本日成交量为本日OBV。一般来说，只是观察OBV的升降并无多大意义，必须配合K线图的走势才有实际的效用。
        由于OBV的计算方法过于简单化，所以容易受到偶然因素的影响，为了提高OBV的准确性，可以采取多空比率净额法对其进行修正。
        多空比率净额= [（收盘价－最低价）－（最高价-收盘价）] ÷（ 最高价－最低价）×V
        该方法根据多空力量比率加权修正成交量，比单纯的OBV法具有更高的可信度。
    """
    __typename__ = "OBV"
    
    def formula(self):
        return Formulas.OBV()
    
    # 公式解析器会调用此方法
    def call(self,M=30):
        f = Formulas.OBV(M)
        if f: return self.parser(f,self.__typename__)