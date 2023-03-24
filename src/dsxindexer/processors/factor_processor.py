from dsxindexer.factors.float_factor import FloatFactor
from dsxindexer.factors.minus_factor import MinusFactor
from dsxindexer.processors.base_processor import BaseProcessor
from dsxindexer.factors.function_factor import FunctionFactor
from dsxindexer.factors.newline_factor import NewlineFactor
from dsxindexer.factors.variable_factor import VariableFactor
from dsxindexer.factors.lparen_factor import LParenFactor
from dsxindexer.factors.string_factor import StringFactor
from dsxindexer.factors.int_factor import IntFactor
from dsxindexer.factors.base_factor import BaseFactor
from dsxindexer.tokenizer import Token
from typing import List

class FactorProcessor(BaseProcessor):

    # 注册factors
    processors:List[BaseFactor] = [
        IntFactor,
        FloatFactor,
        StringFactor,
        LParenFactor,
        VariableFactor,
        NewlineFactor,
        FunctionFactor,
        MinusFactor,
    ]

    def __init__(self) -> None:
        pass

    def call(self,token:Token,parser):
        for item in self.processors:
            if item.type_name==token.type or token.type in item.type_name:
                # 类型匹配，进入处理
                return item(token,parser).call()
        