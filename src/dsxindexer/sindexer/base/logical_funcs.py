"""
逻辑算术函数(IF、CROSS、NOT等)
"""
from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.base_sindexer import BaseSindexer

def IF(self:BaseSindexer,a:DSX_FIELD_STR,b:DSX_FIELD_STR,c:DSX_FIELD_STR=None):
    a = self.GET(a)
    if c==None:
        if a:return a
        else: return self.GET(b)
    if a:return self.GET(b)
    else : return self.GET(c)

def IFF(self:BaseSindexer,a:DSX_FIELD_STR,b:DSX_FIELD_STR,c:DSX_FIELD_STR=None):
    return IF(self,a,b,c)

def IFN(self:BaseSindexer,a:DSX_FIELD_STR,b:DSX_FIELD_STR,c:DSX_FIELD_STR=None):
    a = self.GET(a)
    if c==None:
        if a:return self.GET(b)
        else: return a
    if a:return self.GET(c)
    else : return self.GET(a)

def NOT(self:BaseSindexer,X:DSX_FIELD_STR):
    """求逻辑非

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
    """
    a = self.GET(a)
    return not a

def CROSS(self:BaseSindexer,A:DSX_FIELD_STR,B:DSX_FIELD_STR):
    """交叉函数
    表示当A从下方向上穿过B时返回1,否则返回0
    A：变量或常量，判断交叉的第一条线
    B：变量或常量，判断交叉的第二条线
    CROSS（MA（CLOSE，5），MA（CLOSE，10））5日均线与10日均线金叉；
    CROSS（CLOSE，12）：价格由下向上突破12元

    Args:
        self (BaseSindexer): _description_
        A (DSX_FIELD_STR): _description_
        B (DSX_FIELD_STR): _description_
    """
    AA = self.GET(A)
    BB = self.GET(B)
    RAA = self.GET(A,1)
    RBB = self.GET(B,1)
    if AA==None or BB==None or RAA==None or RBB==None:return 0
    if RAA<=RBB and AA>BB:
        return 1
    return 0

def LONGCROSS(self:BaseSindexer,A:DSX_FIELD_STR,B:DSX_FIELD_STR,N:int):
    """两条线维持一定周期后交叉
    LONGCROSS(A,B,N)表示A在N周期内都小于B，本周期从下方向上穿过B时返1，否则返回0 
    LONGCROSS(MA(CLOSE,5),MA(CLOSE,10),5)表示5日均线维持5周期后与10日均线交金叉

    Args:
        self (BaseSindexer): _description_
        A (DSX_FIELD_STR): _description_
        B (DSX_FIELD_STR): _description_
        N (int): _description_
    """
    # 前N个周期都是A小于B，本周期大于等于B
    AA = self.GET(A)
    BB = self.GET(B)
    if AA>=BB:
        true = 1
        start = max(0,self.cursor.index - N)
        for i in range(start,self.cursor.index):
            RAA = self.GET(A,i)
            RBB = self.GET(B,i)
            if RAA>=RBB: 
                true=0
                break
        return true
    return 0


def UPNDAY(self:BaseSindexer,CLOSE:DSX_FIELD_STR,M:int):
    """
    连涨周期数
    UPNDAY(CLOSE,M)表示连涨M个周期
    UPNDAY(CLOSE,7)表示连涨7天
    """

def DOWNNDAY(self:BaseSindexer,CLOSE:DSX_FIELD_STR,M:int):
    """
    连跌周期数
    UPNDAY(CLOSE,M)表示连跌M个周期
    UPNDAY(CLOSE,7)表示连跌7天
    """

def NDAY(self:BaseSindexer,X:DSX_FIELD_STR,Y:DSX_FIELD_STR,N:int):
    """
    连大
    NDAY(X,Y,N)表示条件X>Y持续存在N个周期
    NDAY(CLOSE,OPEN,3)表示连续3日收阳线
    """

def EXIST(self:BaseSindexer,X:DSX_FIELD_STR,N:int):
    """
    存在
    EXIST(X,N)表示条件X在N周期有存在
    EXIST(CLOSE>OPEN,10)表示前10日内存在着阳线
    """

def EVERY(self:BaseSindexer,X:DSX_FIELD_STR,N:int):
    """
    一直存在
    EVERY(X,N)表示条件X在N周期一直存在
    EVERY(CLOSE>OPEN,10)表示前10日内一直是阳线
    """

def LAST(self:BaseSindexer,X:DSX_FIELD_STR,M:DSX_FIELD_STR,N:DSX_FIELD_STR):
    """
    一直存在
    LAST(X,M,N)表示条件X在前M周期到前N周期存在
    LAST(CLOSE>OPEN,10,5)表示从前10日到前5日内一直阳线。若A为0,表示从第一天开始,B为0,表示到最后日止。
    """