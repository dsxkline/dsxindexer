from dsxindexer.operators.andor_operator import AndOrOperator
from dsxindexer.operators.grealess_operator import GreaLessOperator
from dsxindexer.processors.base_processor import BaseProcessor
from dsxindexer.operators.equal_operator import EqualOperator
from dsxindexer.operators.muldiv_operator import MulDivOperator
from dsxindexer.operators.base_operator import BaseOperator
from dsxindexer.tokenizer import Token
from typing import List

class OperatorProcessor(BaseProcessor):

    # 注册Peratoror
    processors:List[BaseOperator] = [
        # 等号
        EqualOperator,
        # 乘除
        MulDivOperator,
        # 与或
        AndOrOperator,
        # 小于等于
        GreaLessOperator,
    ]

    def __init__(self) -> None:
        pass

    def call(self,token:Token,parser,last_result):
        for item in self.processors:
            if item.type_name==token.type or token.type in item.type_name:
                # 类型匹配，进入处理
                result = item(token,parser,last_result).call()
                if result==None and last_result!=None:result = last_result
                return result
        return last_result
        