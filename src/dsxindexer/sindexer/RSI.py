from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class RSI(BaseSindexer):
    """RSI指标
    相对强弱指标RSI是用以计测市场供需关系和买卖力道的方法及指标。
    计算公式：
    N日RSI =A/（A+B）×100
    A=N日内收盘涨幅之和
    B=N日内收盘跌幅之和（取正值）
    由上面算式可知RSI指标的技术含义，即以向上的力量与向下的力量进行比较，若向上的力量较大，则计算出来的指标上升；若向下的力量较大，则指标下降，由此测算出市场走势的强弱。
    """
    __typename__ = "RSI"

    def formula(self):
        return Formulas.RSI()
    
    # 公式解析器会调用此方法
    def call(self,X:DSX_FIELD_STR,N1=6,N2=12,N3=24):
        f = Formulas.RSI(X,N1,N2,N3)
        if f: return self.parser(f,self.__typename__)