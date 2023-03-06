from dsxindexer.processors.base_processor import BaseProcessor
from dsxindexer.operators.plusminus_operator import PlusMinusOperator
from dsxindexer.operators.equal_operator import EqualOperator
from dsxindexer.operators.muldiv_operator import MulDivOperator
from dsxindexer.operators.base_operator import BaseOperator
from dsxindexer.tokenizer import Token
from typing import List

class OperatorProcessor(BaseProcessor):

    # 注册factors
    processors:List[BaseOperator] = [
        # 等号
        EqualOperator,
        # 乘除
        MulDivOperator,
        # 加减 最后再处理加减
        # PlusMinusOperator,
    ]

    def __init__(self) -> None:
        pass

    def call(self,token:Token,parser,last_result):
        for item in self.processors:
            if item.type_name==token.type or token.type in item.type_name:
                # 类型匹配，进入处理
                result = item(token,parser,last_result).call()
                if not result:result = last_result
                return result
        return last_result
        