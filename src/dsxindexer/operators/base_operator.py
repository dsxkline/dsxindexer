
from dsxindexer.tokenizer import Token
from dsxindexer.configer import TokenType

class BaseOperator:
    # 继承子类需要重写此字段
    type_name:TokenType = None
    def __init__(self,token:Token,parser,last_result) -> None:
        self.token = token
        from dsxindexer.parser import Parser
        self.parser:Parser = parser
        self.last_result = last_result
        pass

    def call(self):
        pass