
from dsxindexer.configer import TokenType
from dsxindexer.tokenizer import Token
from dsxindexer.factors.base_factor import BaseFactor


class FloatFactor(BaseFactor):
    # 设置处理标识类型
    type_name = TokenType.FLOAT

    def call(self):
        # 处理浮点数
        self.parser.eat(self.type_name)
        return float(self.token.value)
        