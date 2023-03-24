
from dsxindexer.configer import TokenType
from dsxindexer.tokenizer import Token
from dsxindexer.factors.base_factor import BaseFactor


class MinusFactor(BaseFactor):
    # 设置处理标识类型
    type_name = TokenType.MINUS

    def call(self):
        op = self.parser.current_token
        self.parser.eat(op.type)
        term = self.parser.factor()
        rs = -term
        return rs
        