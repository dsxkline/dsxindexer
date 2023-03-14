from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class CDP(BaseSindexer):
    """CDP 逆势操作指标
    是反映短线进出的作法，是在一天内同时买进卖出或卖出买进，
    计算方法是
    CDP=（H+L+C*2）÷ 4（H：前一日最高价，L：前一日最低价，C：前一日收市价）。
    """
    __typename__ = "CDP"

    def formula(self):
        return Formulas.CDP()
    
    # 公式解析器会调用此方法
    def call(self):
        f = Formulas.CDP()
        if f: return self.parser(f,self.__typename__)