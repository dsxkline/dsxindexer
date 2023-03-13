from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.fomulas import Formulas
from dsxindexer.sindexer.base_sindexer import BaseSindexer,SindexerResult

class DMI(BaseSindexer):
    """DMI
    DMI指标又叫动向指标或趋向指标，其全称叫“Directional Movement Index，简称DMI”
    计算公式：
    DMI指标的计算方法和过程比较复杂，它涉及到DM、TR、DX等几个计算指标和+DI（即PDI，下同）、-DI（即MDI，下同）、ADX和ADXR等4个研判指标的运算。
    1、计算的基本程序
    以计算日DMI指标为例，其运算的基本程序主要为：
    （1）按一定的规则比较每日股价波动产生的最高价、最低价和收盘价，计算出每日股价的波动的真实波幅、上升动向值、下降动向值TR、+DI、-DI，在运算基准日基础上按一定的天数将其累加，以求n日的TR、+DM和DM值。
    （2）将n日内的上升动向值和下降动向值分别除以n日内的真实波幅值，从而求出n日内的上升指标+DI和下降指标-DI。
    （3）通过n内的上升指标+DI和下降指标-DI之间的差和之比，计算出每日的动向值DX。
    （4）按一定的天数将DX累加后平均，求得n日内的平均动向值ADX。
    （5）再通过当日的ADX与前面某一日的ADX相比较，计算出ADX的评估数值ADXR。
    """
    __typename__ = "DMI"

    def formula(self):
        return Formulas.DMI()
    
    # 公式解析器会调用此方法
    def call(self,N=14,M=6):
        f = Formulas.DMI(N,M)
        if f: return self.parser(f,self.__typename__)