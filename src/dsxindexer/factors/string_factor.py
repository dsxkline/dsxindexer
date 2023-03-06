from dsxindexer.configer import TokenType,ExpreItemDirection
from dsxindexer.tokenizer import Token
from dsxindexer.factors.base_factor import BaseFactor


class StringFactor(BaseFactor):
    # 设置处理标识类型
    type_name = TokenType.STRING

    def call(self):
        # 处理变量命名
        self.parser.eat(self.type_name)
        return str(self.token.value)
        