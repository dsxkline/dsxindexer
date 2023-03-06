# 数学运算操作不是数值字符错误
class DsxindexerNotNumberError(Exception):
    pass
# 找不到方法名错误
class DsxindexerMethodNotFoundError(Exception):
    pass
# 变量命名错误
class DsxindexerVariableNameError(Exception):
    pass

# 一些正则
class RegRolues:
    # 识别变量名称正则
    VARIABLE = r'^[a-zA-Z_][a-zA-Z0-9_]*$'
    VARIABLE_NAME = r'^[a-zA-Z0-9_]*$'
    OPERATIONS = r'^(\+|\-|\*|\/|\%|\=\=|\!\=|\>|\<|\>\=|\<\=|\&\&|\|\|)$'

# Token 类型定义，就是定义表达式字符串每个字符是什么类型
class TokenType:
    # 整形数字
    INTEGER = 'INTEGER'
    # 字符
    STRING = 'STRING'
    # 浮点数
    FLOAT = 'FLOAT'
    # 加号操作符
    PLUS = 'PLUS'
    # 见好操作符
    MINUS = 'MINUS'
    # 乘号操作符
    MUL = 'MUL'
    # 除号操作符
    DIV = 'DIV'
    # 左括号
    LPAREN = 'LPAREN'
    # 右括号
    RPAREN = 'RPAREN'
    # 等于号
    EQUAL = 'EQUAL'
    # 等号左边为变量
    VARIABLE = 'VARIABLE'
    # 换行符
    NEWLINE = "NEWLINE"
    # 函数
    FUNCTION = "FUNCTION"
    # 大于
    GREATERTHEN = "GREATERTHEN"
    # 小于
    LESSTHEN = "LESSTHEN"
    # EOF
    EOF = 'EOF'


# 表达式项的方向，意思是在等号的左边还是右边，用来区分是变量还是表达式
class ExpreItemDirection:
    DEFAULT = 0
    LEFT = 1
    RIGHT = 2

class Cursor:
    index:int = 0
    
# 表达式结束符
EXPR_END_CHART = ";"
# 赋值符号
ASSIGN_CHART = ":="