from dsxindexer.configer import TokenType
from dsxindexer.tokenizer import Token
from dsxindexer.operators.base_operator import BaseOperator

class GreaterThenOperator(BaseOperator):
    # 设置处理标识类型
    type_name = TokenType.GREATERTHEN

    def call(self):
        result = self.last_result
        # 处理大于号
        if self.token.type ==self.type_name:
            self.parser.eat(self.token.type)
            # 是否大于等于,如果下一个是等于符号
            isequal = False
            if self.token.type==self.type_name:
                self.parser.eat(self.token.type)
            # 开始处理右边表达式的值
            result = self.parser.expr()
            if isequal:
                return self.last_result>=result
            else:
                return self.last_result>result
        return result
