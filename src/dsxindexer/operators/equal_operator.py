from dsxindexer.configer import TokenType
from dsxindexer.tokenizer import Token
from dsxindexer.operators.base_operator import BaseOperator

class EqualOperator(BaseOperator):
    # 设置处理标识类型
    type_name = TokenType.EQUAL
    def __init__(self, token: Token,parser,last_result) -> None:
        super().__init__(token,parser,last_result)

    def call(self):
        result = self.last_result
        # 处理等号
        if self.token.type ==TokenType.EQUAL:
            self.parser.eat(self.token.type)
            # 开始处理右边表达式的值
            result = self.parser.expr()
            setattr(self.parser.funcer,self.parser.last_avariable,result)
            # 继续下一个项
            return self.parser.term()
        return result
