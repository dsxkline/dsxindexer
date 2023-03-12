from dsxindexer.configer import TokenType,DsxindexerNotNumberError,logger
from dsxindexer.operators.base_operator import BaseOperator

class PlusMinusOperator(BaseOperator):
    # 设置处理标识类型
    type_name = (TokenType.PLUS,TokenType.MINUS)

    def call(self):
        result = self.last_result
        # 处理加减
        while self.parser.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.parser.current_token
            self.parser.eat(op.type)
            term = self.parser.term()
            if op.type == TokenType.PLUS:
                if term==None:
                    raise DsxindexerNotNumberError("相加因子格式错误,非数字 term=%s TOKEN:%s" % (term,self.parser.current_token.throw_error()))
                if result==None:
                    raise DsxindexerNotNumberError("相加因子格式错误,非数字 result=%s TOKEN:%s" % (result,op.throw_error()))
                
                if isinstance(result,str) or isinstance(term,str):
                    rs = str(result) + str(term)
                else:
                    rs = result + term
                logger.debug("处理相加：%s + %s = %s"%(result,term,rs))
                result = rs
            elif op.type == TokenType.MINUS:
                if not isinstance(term,int) and not isinstance(term,float):
                    raise DsxindexerNotNumberError("相减因子格式错误,非数字 term=%s TOKEN:%s" % (term,self.parser.current_token.throw_error()))
                if not isinstance(result,int) and not isinstance(result,float):
                    # 遇到取反运算等情况处理
                    if self.parser.last_avariable==None:
                        result = 0
                    else:
                        raise DsxindexerNotNumberError("相减因子格式错误,非数字 result=%s TOKEN:%s" % (result,op.throw_error()))
                rs = result - term
                logger.debug("处理相减：%s - %s = %s"%(result,term,rs))
                result = rs
        return result
