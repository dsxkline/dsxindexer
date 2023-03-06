
from dsxindexer.tokenizer import Token
from dsxindexer.configer import TokenType

class BaseFactor:
    # 继承子类需要重写此字段
    type_name:TokenType = None
    def __init__(self,token:Token,parser) -> None:
        self.token = token
        from dsxindexer.parser import Parser
        self.parser:Parser = parser
        pass

    def call(self):
        pass