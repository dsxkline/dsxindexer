from dsxindexer.configer import ExpreItemDirection, TokenType,logger
from dsxindexer.tokenizer import Token
from dsxindexer.operators.base_operator import BaseOperator

class EqualOperator(BaseOperator):
    # 设置处理标识类型
    type_name = TokenType.EQUAL

    def call(self):
        result = self.last_result
        # 处理等号
        if self.token.type ==self.type_name:
            op = self.parser.current_token
            self.parser.eat(op.type)
            # 解析符号右边表达式
            factor = self.parser.factor()
            rs = result == factor
            logger.debug("处理等于条件：%s == %s = %s"%(result,factor,rs))
            result = rs
                
        return result
   