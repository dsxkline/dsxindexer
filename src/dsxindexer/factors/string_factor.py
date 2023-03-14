from dsxindexer.configer import TokenType,ExpreItemDirection
from dsxindexer.tokenizer import Token
from dsxindexer.factors.base_factor import BaseFactor


class StringFactor(BaseFactor):
    # 设置处理标识类型
    type_name = TokenType.STRING

    def call(self):
        # 处理变量命名
        self.parser.eat(self.type_name)
        # 解析点号语法
        strs = str(self.token.value)
        if "." in strs:
            result = ""
            str_list = strs.split(".")
            namespace = str_list[0]
            for item in str_list:
                result = self.parser_point(item,namespace)
            return result

        return strs
        

    def parser_point(self,expre,namespace):
        """解析点号语法"""
        from dsxindexer.tokenizer import Lexer
        from dsxindexer.parser import Parser
        # 词法分析器
        lexer = Lexer(expre,ExpreItemDirection.RIGHT,self.token.location[0])
        # 语法解析器
        parser = Parser(lexer,self.parser.funcer,namespace)
        # 解析并返回结果
        ps = parser.parse()
        return ps.result