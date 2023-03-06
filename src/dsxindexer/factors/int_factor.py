
from dsxindexer.configer import TokenType
from dsxindexer.tokenizer import Token
from dsxindexer.factors.base_factor import BaseFactor


class IntFactor(BaseFactor):
    # 设置处理标识类型
    type_name = TokenType.INTEGER
    def __init__(self, token: Token,parser) -> None:
        super().__init__(token,parser)

    def call(self):
        # 处理整形数字
        self.parser.eat(self.type_name)
        return int(self.token.value)
        