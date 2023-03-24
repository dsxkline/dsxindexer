from dsxindexer.configer import TokenType,DsxindexerNotNumberError,logger
from dsxindexer.operators.base_operator import BaseOperator

class MinusOperator(BaseOperator):
    # 设置处理标识类型
    type_name = TokenType.MINUS

    def call(self):
        result = self.last_result
        # 处理负号
        if self.parser.current_token.type == self.type_name and result==None:
            op = self.parser.current_token
            self.parser.eat(op.type)
            term = self.parser.factor()
            rs = -term
            logger.debug("处理负号：%s - %s = %s"%(result,term,rs))
            result = rs
        return result
