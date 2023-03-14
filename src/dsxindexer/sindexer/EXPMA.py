from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class EXPMA(BaseSindexer):
    """EXPMA 指数平均线
    指数平均数也叫EXPMA指标，它是一种趋向类指标,指数平均数指标是以指数式递减加权的移动平均。其构造原理是对股票收盘价进行算术平均，并根据计算结果来进行分析，用于判断价格未来走势的变动趋势。
    计算公式：
    EXP1:EMA(CLOSE,M1);
    EXP2:EMA(CLOSE,M2);
    """
    __typename__ = "EXPMA"

    def formula(self):
        return Formulas.EXPMA()
    
    # 公式解析器会调用此方法
    def call(self,M1=12,M2=50):
        f = Formulas.EXPMA(M1,M2)
        if f: return self.parser(f,self.__typename__)