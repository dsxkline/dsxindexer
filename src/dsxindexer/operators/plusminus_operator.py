from dsxindexer.operators.base_operator import OperatorNotNumberError
from dsxindexer.configer import TokenType
from dsxindexer.tokenizer import Token
from dsxindexer.operators.base_operator import BaseOperator

class PlusMinusOperator(BaseOperator):
    # 设置处理标识类型
    type_name = (TokenType.PLUS,TokenType.MINUS)
    def __init__(self, token: Token,parser,last_result) -> None:
        super().__init__(token,parser,last_result)

    def call(self):
        result = self.last_result
       # 处理加减
        while self.parser.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.parser.current_token
            self.parser.eat(op.type)
            term = self.parser.term()
            if op.type == TokenType.PLUS:
                if isinstance(result,str) or isinstance(term,str):
                    result = str(result) + str(term)
                else:
                    result = result + term
            elif op.type == TokenType.MINUS:
                if not isinstance(term,int) and not isinstance(term,float):
                    raise OperatorNotNumberError("相减因子格式错误,非数字 term=%s" % term)
                if not isinstance(result,int) and not isinstance(result,float):
                    raise OperatorNotNumberError("相减因子格式错误,非数字 result=%s" % result)
                result = result - term
        return result
