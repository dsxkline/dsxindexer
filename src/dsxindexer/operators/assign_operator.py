from dsxindexer.configer import ExpreItemDirection, TokenType,logger
from dsxindexer.tokenizer import Token
from dsxindexer.operators.base_operator import BaseOperator

class AssignOperator(BaseOperator):
    # 设置处理标识类型
    type_name = TokenType.ASSIGN

    def call(self):
        result = self.last_result
        # 处理等号
        if self.token.type ==TokenType.ASSIGN:
            token = self.token
            if self.token.export:
                self.parser.export.append(self.parser.last_avariable)
            variable = self.parser.last_avariable
            expre = self.token.value
            self.parser.eat(self.token.type)
            # 开始处理右边表达式的值
            result = self.parser_equal(expre,variable)
            logger.debug("正则赋值 %s=%s" % (variable,result))
            # 给变量赋值
            self.parser.funcer.set_value(self.parser.namespace,variable,result,self.parser.func_name)
            # 继续下一个项
            rs = self.parser.term()
            if rs!=None:
                result = rs
        return result
    
    def parser_equal(self,expre,variable):
        """解析等号右边表达式"""
        from dsxindexer.tokenizer import Lexer
        from dsxindexer.parser import Parser
        # 词法分析器
        lexer = Lexer(expre,ExpreItemDirection.RIGHT,self.token.location[0])
        # 语法解析器
        parser = Parser(lexer,self.parser.funcer,self.parser.namespace,func_name=self.parser.func_name)
        parser.last_avariable = variable
        # 解析并返回结果
        ps = parser.parse()
        return ps.result
