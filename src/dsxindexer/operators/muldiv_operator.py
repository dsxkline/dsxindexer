from dsxindexer.configer import TokenType
from dsxindexer.tokenizer import Token
from dsxindexer.operators.base_operator import BaseOperator,OperatorNotNumberError

class MulDivOperator(BaseOperator):
    # 设置处理标识类型
    type_name = (TokenType.MUL,TokenType.DIV)
    def __init__(self, token: Token,parser,last_result) -> None:
        super().__init__(token,parser,last_result)

    def call(self):
        result = self.last_result
        while self.parser.current_token.type in (TokenType.MUL, TokenType.DIV):
            op = self.parser.current_token
            self.parser.eat(op.type)
            factor = self.parser.factor()
            if not isinstance(factor,int) and not isinstance(factor,float):
                raise OperatorNotNumberError("乘除因子格式错误,非数字 %s=%s" % (op,factor))
            if not isinstance(result,int) and not isinstance(result,float):
                raise OperatorNotNumberError("乘除因子格式错误,非数字 %s=%s" % (op,result))
            if op.type == TokenType.MUL:
                result = result * factor
            elif op.type == TokenType.DIV:
                result = result / factor
        return result
