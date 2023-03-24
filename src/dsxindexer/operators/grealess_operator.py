from dsxindexer.configer import TokenType,DsxindexerNotNumberError,logger
from dsxindexer.operators.base_operator import BaseOperator

class GreaLessOperator(BaseOperator):
    # 设置处理标识类型
    type_name = (TokenType.GREATERTHEN,TokenType.GREATERTHEN_EQUAL,TokenType.LESSTHEN,TokenType.LESSTHEN_EQUAL,TokenType.NOTEQUAL)

    def call(self):
        result = self.last_result
        while self.parser.current_token.type in self.type_name:
            op = self.parser.current_token
            self.parser.eat(op.type)
            # 解析符号右边表达式
            factor = self.parser.factor()
            if op.type==TokenType.GREATERTHEN:
                rs = result > factor
                logger.debug("处理大于：%s and %s > %s"%(result,factor,rs))
                result = rs
            if op.type==TokenType.GREATERTHEN_EQUAL:
                rs = result >= factor
                logger.debug("处理大于等于：%s or %s >= %s"%(result,factor,rs))
                result = rs
            if op.type==TokenType.LESSTHEN:
                rs = result < factor
                logger.debug("处理小于：%s and %s > %s"%(result,factor,rs))
                result = rs
            if op.type==TokenType.LESSTHEN_EQUAL:
                rs = result <= factor
                logger.debug("处理小于于等于：%s <= %s = %s"%(result,factor,rs))
                result = rs
            if op.type==TokenType.NOTEQUAL:
                rs = result != factor
                logger.debug("处理不等于：%s != %s = %s"%(result,factor,rs))
                result = rs
        return result
