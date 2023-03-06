import json
import traceback

from dsxindexer.operators.base_operator import OperatorNotNumberError

from dsxindexer.sindexer.base_sindexer import BaseSindexer

from dsxindexer.sindexer.macd import MACD
from dsxindexer.sindexer.kdj import KDJ
from dsxindexer.processors.sindexer_processor import SindexerProcessor
from dsxindexer.functioner import Functioner
from dsxindexer.tokenizer import VariableNameError
from dsxindexer.tokenizer import Lexer
from dsxindexer.parser import Parser
import dsxquant

class ABCD(BaseSindexer):
    """ABCD
    自定义ABCD指标
    """
    # 定义指标名称
    __typename__ = "ABCD"
    # 定义指标导出的变量名
    __exportvars__ = ("A","B","C")

    def formula(self):
        return """
        A:=CLOSE;
        B:=HIGH;
        C:=A*B;
        """
        
if __name__=="__main__":
    try:
        # 获取K线历史数据
        klines = dsxquant.get_klines("000001",dsxquant.market.SZ).datas()
        klines:list = klines.data
        klines.reverse()
        # 指标处理器
        sp = SindexerProcessor(klines)
        # 注册添加一些自定义指标
        sp.register(MACD)
        sp.register(KDJ)
        sp.register(ABCD)
        # 执行计算结果
        result = sp.execute()
        # 取最后一个
        model = result[-1]
        print(model.DATE,vars(model.MACD),vars(model.ABCD))
        pass
        # print(result)  # Output: 11
    except VariableNameError as e:
        print(e)
        pass
    except OperatorNotNumberError as e:
        print(e)
        pass
    except Exception as e:
        traceback.print_exc()