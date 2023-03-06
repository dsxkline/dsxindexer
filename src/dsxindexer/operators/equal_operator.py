from dsxindexer.configer import ExpreItemDirection, TokenType
from dsxindexer.tokenizer import Token
from dsxindexer.operators.base_operator import BaseOperator

class EqualOperator(BaseOperator):
    # 设置处理标识类型
    type_name = TokenType.EQUAL

    def call(self):
        result = self.last_result
        # 处理等号
        if self.token.type ==TokenType.EQUAL:
            expre = self.token.value
            self.parser.eat(self.token.type)
            # 开始处理右边表达式的值
            result = self.parser_equal(expre)
            # setattr(self.parser.funcer,self.parser.last_avariable,result)
            print("正则赋值 %s=%s" % (self.parser.last_avariable,result))
            self.parser.funcer.set_value(self.parser.namespace,self.parser.last_avariable,result)
            # 继续下一个项
            return self.parser.term()
        return result
    
    def parser_equal(self,expre):
        """解析等号右边表达式"""
        from dsxindexer.tokenizer import Lexer
        from dsxindexer.parser import Parser
        # 词法分析器
        lexer = Lexer(expre,ExpreItemDirection.RIGHT)
        # 语法解析器
        parser = Parser(lexer,self.parser.funcer,self.parser.namespace)
        # 解析并返回结果
        ps = parser.parse()
        return ps.result
