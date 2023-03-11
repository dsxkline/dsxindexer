"""
数学函数(MAX、MIN、LN、三角函数等)
统计函数(STD、VAR、AVEDEV等)
横向统计函数
"""
import math
from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.base_sindexer import BaseSindexer

def MAX(self:BaseSindexer,a:DSX_FIELD_STR,b:DSX_FIELD_STR):
    a = self.GET(a)
    b = self.GET(b)
    return max(a,b)

def MIN(self:BaseSindexer,a:DSX_FIELD_STR,b:DSX_FIELD_STR):
    a = self.GET(a)
    b = self.GET(b)
    return min(a,b)

def ABS(self:BaseSindexer,a:DSX_FIELD_STR):
    a = self.GET(a)
    return abs(a)

def SUM(self:BaseSindexer,X:DSX_FIELD_STR,N=1):
    """统计 N 周期中 X 的总和
    SUM(X,N),统计N周期中X的总和,N=0则从第一个有效值开始。
    Args:
        X (DSX_FIELD_STR): _description_
        N (int, optional): _description_. Defaults to 1.
    """
    result = 0
    if N==0: N = self.klines.__len__()
    for i in range(N):
        index = self.cursor.index - i
        if index>=0:
            result += self.GET(X,index)
        else:
            break
    return result

def AVG(self:BaseSindexer,X:DSX_FIELD_STR,N:int=1):
    """返回N周期平均值

    Args:
        X (DSX_FIELD_STR): _description_
        N (int, optional): _description_. Defaults to 1.
    """
    if self.cursor.index<N:return 0
    result = 0
    index = self.cursor.index
    j = 0
    for i in range(N):
        index = self.cursor.index - i
        if index>=0:
            result += self.GET(X,index)
            j += 1
        else:
            break
    return result / j

def AVEDEV(self:BaseSindexer,X:DSX_FIELD_STR,N:int=1):
    """返回X在N周期内的平均绝对偏差。
        AVG = (C+REF(C,1)+REF(C,2))/3
        AVEDEV = (ABS(C-AVG) + ABS(REF(C,1)-AVG) + ABS(REF(C,2)-AVG))/3;
    Args:
        X (DSX_FIELD_STR): 变量名或表达式
        N (int, optional): _description_. Defaults to 1.
    """
    if self.cursor.index<N:return 0
    # N周期均值
    avg = self.AVG(X,N)
    j = 0
    result = 0
    for i in range(N):
        index = self.cursor.index - i
        if index>=0:
            # 计算数据与平均值之间方差的绝对值的总和
            result += abs(self.GET(X,index)-avg)
            j +=1
        else:
            break
        
    return result / j

def STD(self:BaseSindexer,X:DSX_FIELD_STR,N:int=1):
    """计算N周期X的标准差
    Args:
        X (DSX_FIELD_STR): 变量名或表达式
        N (int, optional): _description_. Defaults to 1.
    """
    if self.cursor.index<N:return 0
    # N周期均值
    avg = self.AVG(X,N)
    j = 0
    result = 0
    for i in range(N):
        index = self.cursor.index - i
        if index>=0:
            # 每个样本数据 减去样本全部数据的平均值 的平方相加
            minus = self.GET(X,index)-avg
            result += minus * minus
            j +=1
        else:
            break
    # 标准偏差
    s = math.sqrt(result / (j - 1))
    return s

def DEVSQ(self:BaseSindexer,X:DSX_FIELD_STR,N=1):
    """数据偏差平方和
    数据偏差平方和，求X的N日数据偏差平方和
    DEVSQ(CLOSE,20)，求收盘价的20日数据偏差平方和
    Args:
        X (DSX_FIELD_STR): _description_
        N (int, optional): _description_. Defaults to 1.
    """

def FORCAST(self:BaseSindexer,X:DSX_FIELD_STR,N=1):
    """线性回归预测值
    FORCAST(X,N)为X的N周期线性回归预测值
    FORCAST(CLOSE,10)表示求10周期线性回归预测本周期收盘价
    Args:
        X (DSX_FIELD_STR): _description_
        N (int, optional): _description_. Defaults to 1.
    """

def SLOPE(self:BaseSindexer,X:DSX_FIELD_STR,N=1):
    """线性回归斜率
    SLOPE(X,N)为X的N周期线性回归线的斜率
    SLOPE(CLOSE,10)表示求10周期线性回归线的斜率
    Args:
        X (DSX_FIELD_STR): _description_
        N (int, optional): _description_. Defaults to 1.
    """

def STDP(self:BaseSindexer,X:DSX_FIELD_STR,N=1):
    """总体标准差
    STDP(X,N)为X的N日总体标准差
    STDP(CLOSE,20)，求收盘价的20日总体标准差
    Args:
        X (DSX_FIELD_STR): _description_
        N (int, optional): _description_. Defaults to 1.
    """

def VAR(self:BaseSindexer,X:DSX_FIELD_STR,N=1):
    """估算样本方差
    VAR(X,N)为X的N日估算样本方差
    VAR(CLOSE,20)，求收盘价的20日总体标准差
    Args:
        X (DSX_FIELD_STR): _description_
        N (int, optional): _description_. Defaults to 1.
    """

def VARP(self:BaseSindexer,X:DSX_FIELD_STR,N=1):
    """体样本方差
    VARP(X,N)为X的N日总体样本方差
    VARP(CLOSE,20)，求收盘价的20日总体样本方差
    Args:
        X (DSX_FIELD_STR): _description_
        N (int, optional): _description_. Defaults to 1.
    """


def COUNT(self:BaseSindexer,X:DSX_FIELD_STR,N=1):
    """统计总数统计满足条件的周期数。
    COUNT(X,N),统计N周期中满足X条件的周期数,若N=0则从第一个有效值开始。
    COUNT(CLOSE>OPEN,20)表示统计20周期内收阳的周期数
    Args:
        X (DSX_FIELD_STR): _description_
        N (int, optional): _description_. Defaults to 1.
    """
    result = 0
    if N==0: N = self.klines.__len__()
    for i in range(N):
        index = self.cursor.index - i
        if index>=0:
            result += self.GET(X,index)==True and 1 or 0
        else:
            break
    return result


def BETWEEN(self:BaseSindexer,A:DSX_FIELD_STR,B:DSX_FIELD_STR,C:DSX_FIELD_STR):
    """介于(介于两个数之间)
    用法:BETWEEN(A,B,C)表示A处于B和C之间时返回1，否则返回0
    BETWEEN(CLOSE,MA(CLOSE,10),MA(CLOSE,5))表示收盘价介于5日均线和10日均线之间

    Args:
        self (BaseSindexer): _description_
        A (DSX_FIELD_STR): _description_
        B (DSX_FIELD_STR): _description_
        C (DSX_FIELD_STR): _description_
    """

def MOD(self:BaseSindexer,A:DSX_FIELD_STR,B:DSX_FIELD_STR):
    """求模运算
    MOD(A,B)返回A对B求模
    MOD(26,10)返回6 

    Args:
        self (BaseSindexer): _description_
        A (DSX_FIELD_STR): _description_
        B (DSX_FIELD_STR): _description_
    """

def RANGE(self:BaseSindexer,A:DSX_FIELD_STR,B:DSX_FIELD_STR,C:DSX_FIELD_STR):
    """范围(于某个范围之间)
    RANGE(A,B,C)表示A大于B同时小于C时返回1，否则返回0 
    RANGE(CLOSE,MA(CLOSE,5),MA(CLOSE,10))表示收盘价大于5日均线并且小于10日均线

    Args:
        self (BaseSindexer): _description_
        A (DSX_FIELD_STR): _description_
        B (DSX_FIELD_STR): _description_
        C (DSX_FIELD_STR): _description_
    """

def REVERSE(self:BaseSindexer,X:DSX_FIELD_STR):
    """求相反数
    REVERSE(X)返回-X 
    REVERSE(CLOSE)返回-CLOSE 

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
    """
    XX = self.GET(X)
    if XX!=None:
        return -XX
def SGN(self:BaseSindexer,X:DSX_FIELD_STR):
    """求符号值
    用法:SGN(X)，当X>0,X=0,X<0分别返回1,0,-1
    SGN(10)返回1，SGN(0)返回0，SGN(-10)返回-1 

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
    """

def ACOS(self:BaseSindexer,X:DSX_FIELD_STR):
    """反余弦值
    ACOS(X)返回X的反余弦值
    ACOS(CLOSE)返回CLOSE的反余弦值

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
    """

def ASIN(self:BaseSindexer,X:DSX_FIELD_STR):
    """反正弦值
    ASIN(X)返回X的反正弦值
    ASIN(CLOSE)返回CLOSE的反正弦值

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
    """

def CEILING(self:BaseSindexer,X:DSX_FIELD_STR):
    """向上舍入(向数值增大方向舍入)
    CEILING(A)返回沿A数值增大方向最接近的整数
    CEILING(12.3)求得13；
    CEILING(-3.5)求得-3

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
    """

def COS(self:BaseSindexer,X:DSX_FIELD_STR):
    """余弦值
    COS(X)返回X的余弦值
    COS(CLOSE)返回收盘价的余弦值

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
    """

def EXP(self:BaseSindexer,X:DSX_FIELD_STR):
    """指数
    EXP(X)为e的X次幂
    EXP(CLOSE)返回e的CLOSE次幂

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
    """

def FLOOR(self:BaseSindexer,X:DSX_FIELD_STR):
    """向下舍入(向数值减小方向舍入)
    FLOOR(A)返回沿A数值减小方向最接近的整数
    FLOOR(12.3)求得12；
    FLOOR(-3.5)求得-4

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
    """

def INTPART(self:BaseSindexer,X:DSX_FIELD_STR):
    """取整(绝对值减小取整，即取得数据的整数部分)
    INTPART(A)返回沿A绝对值减小方向最接近的整数
    INTPART(12.3)求得12,INTPART(-3.5)求得-3 

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
    """

def LN(self:BaseSindexer,X:DSX_FIELD_STR):
    """求自然对数
    LN(X)以e为底的对数
    LN(CLOSE)求收盘价的对数

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
    """

def LOG(self:BaseSindexer,X:DSX_FIELD_STR):
    """以10为底的对数
    LOG(X)取得X的对数
    LOG(100)等于10 

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
    """

def POW(self:BaseSindexer,X:DSX_FIELD_STR):
    """乘幂
    POW(A,B)返回A的B次幂
    POW(CLOSE,3)求得收盘价的3次方

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
    """

def SIN(self:BaseSindexer,X:DSX_FIELD_STR):
    """正弦值
    SIN(X)返回X的正弦值
    SIN(CLOSE)返回CLOSE的正弦值

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
    """

def SQRT(self:BaseSindexer,X:DSX_FIELD_STR):
    """开平方
    SQRT(X)为X的平方根
    SQRT(CLOSE)收盘价的平方根

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
    """

def TAN(self:BaseSindexer,X:DSX_FIELD_STR):
    """正切值
    TAN(X)返回X的正切值
    TAN(CLOSE)返回CLOSE的正切值

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
    """