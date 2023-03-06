import re
import dsxindexer.configer as configer
from dsxindexer.configer import ExpreItemDirection,TokenType,DsxindexerVariableNameError


# Token类定义
class Token:
    def __init__(self, type, value,direction:ExpreItemDirection=ExpreItemDirection.DEFAULT):
        self.type = type
        self.value = value
        self.direction:ExpreItemDirection = direction
        # print(self.__repr__())

    def __repr__(self):
        return 'Token({type}, {value},{direction})'.format(
            type=self.type,
            value=repr(self.value),
            direction=repr(self.direction)
        )


# 词法分析器类定义
# 主要功能是解析字符表达式的每个字符，生成记号TOKEN序列，并提供记号流转
class Lexer:
    def __init__(self, text,direction:ExpreItemDirection=ExpreItemDirection.LEFT):
        self.text = text
        self.pos = 0
        self.current_char:str = self.text[self.pos]
        # 目前是在等号的左边还是右边，默认在左边，用来判断是变量名称还是字符串
        # 如果解析函数内部参数，则需要手动传右边
        self.direction = direction

    # 辅助函数，用于向前移动指针并更新当前字符
    def next(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]

    # 辅助函数，用于跳过空白字符
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.next()

    # 辅助函数，用于解析一个整数
    def integer(self):
        result = ''
        while self.current_char is not None:
            if self.current_char.isdigit() :
                result += self.current_char
            elif self.current_char == ".":
                # 处理浮点数
                result += self.current_char
                self.next()
                return self.floater(result)
            else:
                break
            self.next()
        return Token(TokenType.INTEGER, int(result),self.direction)
    
    def floater(self,result):
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.next()
        return Token(TokenType.INTEGER, float(result),self.direction)

    # 提取变量名
    def variable(self):
        # 遇到等号和换行符以及操作符都必须退出
        result = ''
        while self.current_char is not None and self.current_char not in configer.ASSIGN_CHART and self.current_char!=configer.EXPR_END_CHART and not self.current_char.isspace() and not re.match(configer.RegRolues.OPERATIONS,self.current_char):
            if re.match(configer.RegRolues.VARIABLE_NAME,self.current_char):
                result += self.current_char
            else:
                # 遇到括号就是函数
                if self.current_char == "(":
                    return self.get_function(str(result))
                if self.current_char == ")":break
                # 如果变量名含有特殊字符，报错
                raise DsxindexerVariableNameError("变量命名错误，含有特殊字符：%s" % self.current_char) 
            self.next()
        return Token(TokenType.VARIABLE, str(result),self.direction)
    
    def get_function(self,func_name):
        """识别为函数的时候，方向需要指向等号右边，否则无法获取到变量值
        """
        self.direction = ExpreItemDirection.RIGHT
        # 处理函数
        result = ''
        i = 0
        while self.current_char is not None and self.current_char!=configer.EXPR_END_CHART:
            result += self.current_char
            # 遇到括号就是函数结束了,需要解析到最后一个括号
            if self.current_char == "(": i+=1
            if self.current_char == ")":
                i -=1
                if i<=0:
                    self.next()
                    break
            self.next()
            
        return Token(TokenType.FUNCTION, func_name+str(result),self.direction)

    
    # 提取字符串，有可能是变量或者字符串值
    def string(self):
        # 遇到换行符必须退出
        result = ''
        self.next()
        while self.current_char is not None and self.current_char!=configer.EXPR_END_CHART and self.current_char!="\"" and self.current_char!="\'":
            result += self.current_char
            self.next()
        self.next()
        return str(result)
    
    # 提取括号
    def paren(self):
        # 遇到匹配的右括号就结束
        result = ''
        i = 1
        while self.current_char is not None and self.current_char!=configer.EXPR_END_CHART:
            # 遇到括号就是函数结束了,需要解析到最后一个括号
            if self.current_char == "(":i+=1
            if self.current_char == ")":
                i -=1
                if i<=0:
                    self.next()
                    break
            result += self.current_char

            self.next()
        return Token(TokenType.LPAREN, str(result),self.direction)
    
    def assign(self):
        result = ''
        # 处理赋值符号
        while self.current_char is not None and self.current_char!=configer.EXPR_END_CHART:
            # 先跳过赋值符号
            for i in range(len(configer.ASSIGN_CHART)-1):
                self.next()
            result += self.current_char
            
        return Token(TokenType.EQUAL, result,ExpreItemDirection.DEFAULT)

    # 核心函数，用于将输入的字符序列分割为一个个Token
    def get_next_token(self):
        while self.current_char is not None:
            # 换行符
            if self.current_char == configer.EXPR_END_CHART:
                self.next()
                # 进入等号左边
                self.direction = ExpreItemDirection.LEFT
                return Token(TokenType.NEWLINE, configer.EXPR_END_CHART,self.direction)
            # 赋值符号
            if self.current_char in configer.ASSIGN_CHART:
                self.next()
                # 进入等号右边
                self.direction = ExpreItemDirection.RIGHT
                return self.assign()
            
            # 右括号不需要处理
            if self.current_char == ')':
                self.next()
                continue
            # 跳过空格
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # 设别数字字符
            if self.current_char.isdigit():
                return self.integer()

            # 识别加减乘除算数表达式符号
            if self.current_char == '+':
                # 移动字符
                self.next()
                return Token(TokenType.PLUS, "+",self.direction)

            if self.current_char == '-':
                self.next()
                return Token(TokenType.MINUS, "-",self.direction)

            if self.current_char == '*':
                self.next()
                return Token(TokenType.MUL, "*",self.direction)

            if self.current_char == '/':
                self.next()
                return Token(TokenType.DIV, "/",self.direction)

            if self.current_char == '(':
                self.next()
                return self.paren()
            
            if self.current_char == '>':
                self.next()
                return Token(TokenType.GREATERTHEN, ">",self.direction)
            
            if self.current_char == '<':
                self.next()
                return Token(TokenType.GREATERTHEN, "<",self.direction)
            
            # 单引号或者双引号开头的解析为字符串
            if self.current_char == '\"' or self.current_char == '\'':
                return Token(TokenType.STRING, self.string(),self.direction)
            
            # 字母开头数字下划线组合的变量
            if re.match(configer.RegRolues.VARIABLE, self.current_char):
                # 设别变量
                return self.variable()

            raise ValueError('Invalid character: ' + self.current_char,self.direction)

        return Token(TokenType.EOF, None)
