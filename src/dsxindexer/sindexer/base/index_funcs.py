"""指标函数(PEAK、SAR、COSET、WINNER、ZIG等)
"""

from dsxindexer.configer import DSX_FIELD_STR
from dsxindexer.sindexer.base_sindexer import BaseSindexer

def MA(self:BaseSindexer,X:DSX_FIELD_STR="CLOSE",N=5):
    """MA指标是英文(Moving average)的简写，叫移动平均线指标。
    1.N日MA=N日收市价的总和/N(即算术平均数)
    
    """
    amount = 0
    if isinstance(N,float):N = int(N)
    if self.cursor.index - N<0:return 0
    start = max(0,self.cursor.index - N)+1
    end = self.cursor.index+1
    M = 0
    for i in range(start,end):
        amount += self.GET(X,i)
        M += 1
    if M==0: ma = self.GET(X)
    else: ma = amount / M
    return ma

def DMA(self:BaseSindexer,X:DSX_FIELD_STR,N:float):
    """动态移动平均求动态移动平均。
    若Y=DMA(X,A)则Y=A*X+(1-A)*Y',其中Y'表示上一周期Y值,A必须小于1。
    DMA(CLOSE,VOL/CAPITAL)表示求以换手率作平滑因子的平均价

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
        N (float): _description_
    """

def EMA(self:BaseSindexer,X:DSX_FIELD_STR,N:int=1):
    """指数平滑移动平均卖一价求指数平滑移动平均。
    若Y=EMA(X,N)则Y=[2*X+(N-1)*Y']/(N+1),其中Y'表示上一周期Y值。
    EMA(CLOSE,30)表示求30日指数平滑均价
    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
        N (int): _description_
    """
    XX = self.GET(X)
    alpha = 2/(N+1)
    last_key = str(X)+"_EMA_"+str(N)
    if self.cursor.index==0 : 
        ema = XX
    else:
        last_ema = self.REF(last_key)
        ema = (1.0-alpha)*last_ema + alpha * XX
    self.save_temp(last_key,ema)
    return ema

def SMA(self:BaseSindexer,X:DSX_FIELD_STR,N,M):
    """SMA（Simple moving average(SMA)）简单移动平均线是一种最基础的技术指标。
    SMA 的计算公式如下：
    SMA(X,N,M) 求X的N日移动平均，M为权重。
    算法：
    若Y=SMA(X,N,M) 则 Y=(M*X+(N-M)*Y')/N，其中Y'表示上一周期Y值，N必须大于M。
    
    """
    XX = self.GET(X)
    if N<=M: return
    last_key = "LY"+str(N)+str(X)
    LY = self.REF(last_key)
    if LY==None: LY = XX
    Y = (M*XX+(N-M)*LY)/N
    self.save_temp(last_key,Y)
    return Y

def COST(self:BaseSindexer,X:float):
    """成本分布
    COST(X)表示X%获利盘的价格是多少
    COST(10),表示10%获利盘的价格是多少，即有10%的持仓量在该价格以下，其余90%在该价格以上，为套牢盘该函数仅对日线分析周期有效
    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
        N (int): _description_
    """

def PEAK(self:BaseSindexer,K,N,M):
    """前M个ZIG转向波峰值，属于未来函数
    PEAK(K,N,M)表示之字转向ZIG(K,N)的前M个波峰的数值,M必须大于等于1 
    PEAK(0,5,1)表示%5开盘价ZIG转向的上一个波峰到当前的周期数
    """

def PEAKBARS(self:BaseSindexer,K,N,M:int):
    """前M个ZIG转向波峰到当前距离，属于未来函数
    PEAKBARS(K,N,M)表示之字转向ZIG(K,N)的前M个波峰到当前的周期数,M必须大于等于1
    PEAKBARS(0,5,1)表示%5开盘价ZIG转向的上一个波峰到当前的周期数
    """

def SAR(self:BaseSindexer,N:int,S,M):
    """抛物转向
    SAR(N,S,M),N为计算周期,S为步长,M为极值
    SAR(10,2,20)表示计算10日抛物转向，步长为2%，极限值为20%
    """

def SARTURN(self:BaseSindexer,N:int,S,M):
    """抛物转向点
    用法:SARTURN(N,S,M),N为计算周期,S为步长,M为极值,若发生向上转向则返回1,若发生向下转向则返回-1,否则为0
    """

def TROUGH(self:BaseSindexer,K:int,N:float,M:int):
    """前M个波谷值（前M个ZIG转向波谷值）
    TROUGH(K,N,M)表示之字转向ZIG(K,N)的前M个波谷的数值,M必须大于等于1 
    TROUGH(2,5,2)表示%5最低价ZIG转向的前2个波谷的数值
    """

def TROUGHBARS(self:BaseSindexer,K:int,N:float,M:int):
    """前M个波谷位置
    TROUGHBARS(K,N,M)表示之字转向ZIG(K,N)的前M个波谷到当前的周期数,M必须大于等于1
    TROUGHBARS(2,5,2)表示%5最低价ZIG转向的前2个波谷到当前的周期数
    """

def WINNER(self:BaseSindexer,CLOSE:float):
    """获利盘比例
    WINNER(CLOSE),表示以当前收市价卖出的获利盘比例，该函数仅对日线分析周期有效
    返回0.1表示10%获利盘；WINNER(10.5)表示10.5元价格的获利盘比例。
    """

def ZIG(self:BaseSindexer,K:int,N:float):
    """之字转向 属于未来函数
    ZIG(K,N),当价格变化量超过N%时转向,K表示0:开盘价,1:最高价,2:最低价,3:收盘价
    ZIG(3,5)表示收盘价的5%的ZIG转向
    """
def ZIGA(self:BaseSindexer,K:int,N:float):
    """反向之字转向 属于未来函数
    用法:
    ZIGA(K,X),当价格变化超过X时转向,K表示0:开盘价,1:最高价,2:最低价,3:收盘价,其余:数组信息
    例如:
    ZIGA(3,1.5)表示收盘价变化1.5元的ZIGA转向
    """

def COSTEX(self:BaseSindexer,A:DSX_FIELD_STR,B:DSX_FIELD_STR):
    """区间成本
    COSTEX(A,B),表示两日收盘价格间筹码的成本
    COSTEX(CLOSE,REF(CLOSE)),表示近两日收盘价格间筹码的成本.返回10表示区间成本为10元.
    """

def PWINNER(self:BaseSindexer,N:int,X:DSX_FIELD_STR):
    """远期获利盘比例
    PWINNER(N,X)表示N天前的那部分成本以当前收市价卖出的获利盘比例
    PWINNER(5,CLOSE),表示5天前的那部分成本以当前收市价卖出的获利盘比例，例如返回0.1表示10%获利盘.该函数仅对日线分析周期有效.
    """

def LWINNER(self:BaseSindexer,N:int,X:DSX_FIELD_STR):
    """近期获利盘比例
    LWINNER(N,X)表示最近5天的那部分成本以当前收市价卖出的获利盘比例
    LWINNER(5,CLOSE),表示最近5天的那部分成本以当前收市价卖出的获利盘比例，例如返回0.1表示10%获利盘.该函数仅对日线分析周期有效.
    """

def PPART(self:BaseSindexer,N:int):
    """远期成本分布比例
    PPART(N)表示N天前的成本占总成本的比例
    PPART(10),表示10前的成本占总成本的比例，返回0.2表示20%
    """