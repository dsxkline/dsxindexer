from dsxindexer.configer import TokenType,DsxindexerNotNumberError,logger
from dsxindexer.operators.base_operator import BaseOperator

class MulDivOperator(BaseOperator):
    # 设置处理标识类型
    type_name = (TokenType.MUL,TokenType.DIV,TokenType.PERCENT)

    def call(self):
        result = self.last_result
        while self.parser.current_token.type in self.type_name:
            op = self.parser.current_token
            self.parser.eat(op.type)
            # 解析乘号的右边表达式
            factor = self.parser.factor()
            if not isinstance(factor,int) and not isinstance(factor,float):
                raise DsxindexerNotNumberError("乘除因子格式错误,非数字 %s" % self.parser.current_token.throw_error())
            if not isinstance(result,int) and not isinstance(result,float):
                raise DsxindexerNotNumberError("乘除因子格式错误,非数字 %s" % (op.throw_error()))
            if op.type==TokenType.MUL:
                rs = result * factor
                logger.debug("处理相乘：%s * %s = %s"%(result,factor,rs))
                result = rs
            if op.type==TokenType.DIV:
                if factor!=0:rs = result / factor
                else:rs = 0
                logger.debug("处理相除：%s / %s = %s"%(result,factor,rs))
                result = rs
            if op.type==TokenType.PERCENT:
                if factor!=0:rs = result % factor
                else:rs = 0
                logger.debug("处理取余：%s / %s = %s"%(result,factor,rs))
                result = rs
            
        return result
