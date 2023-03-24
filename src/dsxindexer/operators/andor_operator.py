from dsxindexer.configer import TokenType,DsxindexerNotNumberError,logger
from dsxindexer.operators.base_operator import BaseOperator

class AndOrOperator(BaseOperator):
    # 设置处理标识类型
    type_name = (TokenType.AND,TokenType.OR,TokenType.NOT)

    def call(self):
        result = self.last_result
        while self.parser.current_token.type in (TokenType.AND,TokenType.OR,TokenType.NOT):
            op = self.parser.current_token
            self.parser.eat(op.type)
            # 解析符号右边表达式
            factor = self.parser.term()
            if op.type==TokenType.AND:
                rs = result and factor
                logger.debug("处理与：%s and %s = %s"%(result,factor,rs))
                result = rs
            if op.type==TokenType.OR:
                rs = result or factor
                logger.debug("处理或：%s or %s = %s"%(result,factor,rs))
                result = rs
            if op.type==TokenType.NOT:
                rs = not factor
                logger.debug("处理非：not %s = %s"%(factor,rs))
                result = rs
        return result
