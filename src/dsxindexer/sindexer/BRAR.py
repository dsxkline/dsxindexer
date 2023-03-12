from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class BRAR(BaseSindexer):
    """BRAR 情绪指标 BRAR指标也称为人气意愿指标，又称为能量指标
    计算方法：
        1.AR指标的计算方法
        AR指标是通过比较一段周期内的开盘价在该周期价格中的高低。从而反映市场买卖人气的技术指标。
        以计算周期为日为例，其计算公式为：
        N日AR=(N日内（H－O）之和除以N日内（O－L）之和)*100
        其中，H为当日最高价，L为当日最低价，O为当日开盘价，N为设定的时间参数，一般原始参数日设定为26日
        2.BR指标的计算方法
        BR指标是通过比较一段周期内的收盘价在该周期价格波动中的地位，来反映市场买卖意愿程度的技术指标。
        以计算周期为日为例，其计算公式为：
        N日BR=N日内（H－CY）之和除以N日内（CY－L）之和*100
        其中，H为当日最高价，L为当日最低价，CY为前一交易日的收盘价，N为设定的时间参数，一般原始参数日设定为26日。
    """
    __typename__ = "BRAR"
    
    def formula(self):
        return Formulas.BRAR()
    
    # 公式解析器会调用此方法
    def call(self,N=26):
        f = Formulas.BRAR(N)
        if f: return self.parser(f,self.__typename__)