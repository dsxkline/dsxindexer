from dsxindexer.configer import TokenType,DsxindexerNotNumberError
from dsxindexer.operators.base_operator import BaseOperator

class PlusMinusOperator(BaseOperator):
    # 设置处理标识类型
    type_name = (TokenType.PLUS,TokenType.MINUS)

    def call(self):
        result = self.last_result
       # 处理加减
        if self.parser.current_token.type in (TokenType.PLUS, TokenType.MINUS):
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
                    raise DsxindexerNotNumberError("相减因子格式错误,非数字 term=%s TOKEN:%s" % (term,self.parser.current_token))
                if not isinstance(result,int) and not isinstance(result,float):
                    raise DsxindexerNotNumberError("相减因子格式错误,非数字 result=%s TOKEN:%s" % (result,self.parser.current_token))
                result = result - term
        return result
