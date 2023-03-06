from dsxindexer.configer import TokenType,ExpreItemDirection
from dsxindexer.tokenizer import Token
from dsxindexer.factors.base_factor import BaseFactor


class ParenFactor(BaseFactor):
    # 设置处理标识类型
    type_name = TokenType.LPAREN
    def __init__(self, token: Token,parser) -> None:
        super().__init__(token,parser)

    def call(self):
        # 处理括号
        self.parser.eat(self.type_name)
        # 处理括号表达式
        result = self.parser.expr()
        # 吃掉右边的括号结束
        self.parser.eat(TokenType.RPAREN)
        return result

        