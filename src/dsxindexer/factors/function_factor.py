import re
from dsxindexer.processors.base_processor import BaseProcessor
from dsxindexer.configer import TokenType,ExpreItemDirection
from dsxindexer.tokenizer import Token
from dsxindexer.factors.base_factor import BaseFactor


class FunctionFactor(BaseFactor):
    # 设置处理标识类型
    type_name = TokenType.FUNCTION

    def __init__(self, token: Token,parser) -> None:
        super().__init__(token,parser)

    def call(self):
        # 处理函数
        self.parser.eat(self.type_name)
        # 解析函数并返回值
        result = self.parser_func(self.token.value)
        # 解析完函数后，需要继续，有些函数没有返回值会返回 None，需要特殊处理
        if result==None: return self.parser.factor()
        return result
    
    def parser_func(self,expre):
        funcs = self.parse_function(expre)
        if funcs:
            func_name = funcs[0]
            func_args = funcs[1]
            args = []
            for item in func_args:
                args.append(self.parser_func_args(item))
                pass
            # 寻找可调用方法
            methods = [method_name for method_name in dir(self.parser.funcer) if callable(getattr(self.parser.funcer, method_name)) and not method_name.startswith('__')]
            # 通过方法名获取方法对象
            if func_name in methods:
                method = methods[func_name]
            # 如果找不到，去函数扩展库找
            else:
                for c in self.parser.funcer.function_exs:
                    obj = c
                    # 检查对象是否已实例化
                    if type(obj)==type: obj = c()
                    # 否则直接查找类的方法
                    if type(obj).__name__ == func_name:
                        method = getattr(obj,"call")
                        break
                        
                    del obj

            # 调用方法
            return method(*args)
    
    def parser_func_args(self,expre):
        """解析函数参数"""
        from dsxindexer.tokenizer import Lexer
        from dsxindexer.parser import Parser
        # 词法分析器
        lexer = Lexer(expre,ExpreItemDirection.RIGHT)
        # 语法解析器
        parser = Parser(lexer,self.parser.funcer)
        # 解析并返回结果
        ps = parser.parse()
        return ps.result
        
    def parse_function(self,text):
        pattern = r'(\w+)\((.*)\)'
        match = re.match(pattern, text)
        if match:
            function_name = match.group(1)
            arguments = match.group(2).split(',')
            arguments = [arg.strip() for arg in arguments]
            return (function_name,arguments)
        else:
            return None

        