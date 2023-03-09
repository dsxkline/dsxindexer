from dsxindexer.configer import TokenType,ExpreItemDirection,logger
from dsxindexer.tokenizer import Token
from dsxindexer.factors.base_factor import BaseFactor


class LParenFactor(BaseFactor):
    # 设置处理标识类型
    type_name = TokenType.LPAREN

    def call(self):
        # 处理括号
        # logger.debug("开始处理括号：%s"%self.parser.current_token.value)
        # self.parser.eat(self.type_name)
        # 处理括号表达式 例如 RSV:=(CLOSE-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100; 需要解决从左到右的问题
        result = self.parser_paren(self.parser.current_token.value)
        logger.debug("处理完括号：%s = %s"%(self.parser.current_token.value,result))
        self.parser.eat(self.type_name)
        # 吃掉右边的括号结束
        # self.parser.eat(TokenType.RPAREN)
        return result
    
    def parser_paren(self,expre):
        """解析函数参数"""
        from dsxindexer.tokenizer import Lexer
        from dsxindexer.parser import Parser
        # 词法分析器
        lexer = Lexer(expre,ExpreItemDirection.RIGHT,self.token.location[0])
        # 语法解析器
        parser = Parser(lexer,self.parser.funcer,self.parser.namespace,func_name=self.parser.func_name)
        # 解析并返回结果
        ps = parser.parse()
        return ps.result

        