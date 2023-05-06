"""指标函数(PEAK、SAR、COSET、WINNER、ZIG等)
"""

import math
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

def DMA(self:BaseSindexer,X:DSX_FIELD_STR,A:float):
    """动态移动平均求动态移动平均。
    若Y=DMA(X,A)则Y=A*X+(1-A)*Y',其中Y'表示上一周期Y值,A必须小于1。
    DMA(CLOSE,VOL/CAPITAL)表示求以换手率作平滑因子的平均价

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
        N (float): _description_
    """
    XX = self.GET(X)
    last_key = str(X)+"_DMA_"+str(A)
    if self.cursor.index==0 : 
        dma = XX
    else:
        last_dma = self.REF(last_key)
        dma = A*XX+(1-A)*last_dma
    self.save_temp(last_key,dma)
    return dma

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
    COST函数主要是从图表上最左边的bar开始统计到当根bar，每根bar取一个价格样本(这里取的是开盘价与收盘价的中间价作为样本)和成交量样本，建立两个数组分别存储价格样本、成交量样本与价格样本的乘积；之后对价格样本进行排序，然后通过对价格样本for循环来查找使1%的获利盘的价格。

    Args:
        self (BaseSindexer): _description_
        X (DSX_FIELD_STR): _description_
        N (int): _description_
    """
    pvs = {}
    amount = 0
    for i in range(self.cursor.index+1):
        o = self.klines[i]
        p = (o.CLOSE + o.OPEN)/2
        a = o.VOL * p
        amount += a
        pvs[str(p)+"-"+str(i)] = a
    ps = list(pvs.keys())
    ps.sort()
    pr = 0
    price = 0
    for i in range(ps.__len__()):
        k = ps[i]
        p = float(k.split("-")[0])
        vp = pvs.get(k)
        pr += vp
        if pr/amount>=X/100:
            price = p
            break
    return price

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

def SAR(self:BaseSindexer,N:int,S:int,M:int):
    """抛物转向
    SAR（i）= SAR（i-1）+ AF（i）×（EP（i-1）- SAR（i-1））
    SAR(N,S,M),N为计算周期,S为步长,M为极值
    SAR(10,2,20)表示计算10日抛物转向，步长为2%，极限值为20%
    """
    if self.cursor.index<N-1: return
    # 这个key主要用来保存上一个计算值
    last_key = ""+str(N)+"_"+str(S)+"_"+str(M)
    # 取得第一个K线下标
    start = max(0,self.cursor.index - N+1)
    close = self.CLOSE
    high = self.HIGH
    low = self.LOW
    # EP值
    ep = 0
    # AF值
    af = 0.0
    # SAR值
    sar = 0
    # 第一个收盘价
    close_0 = self.GET("CLOSE",start)
    # 若Tn周期为上涨趋势，EP(Tn-1)为Tn-1周期的最高价，若Tn周期为下跌趋势，EP(Tn-1)为Tn-1周期的最 低价；
    max_high = self.HHV("HIGH",N)
    min_low = self.LLV("LOW",N)
    # 确定趋势
    # 第一个T0日的趋势 上涨=1 下跌=0
    # 初始值SAR(T0)的确定
    # 若T1周期中SAR(T1)上涨趋势，则SAR(T0)为T0周期的最低价，若T1周期下跌趋势，则SAR(T0)为T0周期 的最高价；
    qushi = True
    if (close>close_0):
        ep = max_high
        qushi = True
        # 看涨行情第一个sar为周期内的最低价
        sar = min_low
    else:
        qushi = False
        ep = min_low
        # 看跌行情第一个sar为周期内的最高价
        sar = max_high
    # 上一个SAR值
    last_sar = self.REF("SAR"+last_key)
    # 这里会直接从计算第二个sar开始
    if(last_sar) :
        # 上一个趋势
        ll_qushi = self.REF("QS"+last_key)
        # 如果上涨趋势当前的最低价小于 sar ，则表明进入反转下跌
        if ll_qushi and low<=last_sar:
            ep = min_low
            sar = max_high
            af = 0
            # 周期反转
            qushi = not ll_qushi
        elif not ll_qushi and high>=last_sar:
            # 如果下跌趋势当前的最高价大于sar ，则表明进入反转上涨
            ep = max_high
            sar = min_low
            af = 0
            # 周期反转
            qushi = not ll_qushi
        else:
            # 抛物线的趋势判断需要跟上一个sar值进行判断，跟第一个TO值趋势判断不同
            # 当前收盘价>N日前的收盘价 看涨
            # 极点价EP的确定
            if close>last_sar:
                ep = max_high
                qushi = True
            else:
                qushi = False
                ep = min_low
            # 上一个周期的值
            l_high = self.REF("HIGH")
            l_low = self.REF("LOW")
            last_af = self.REF("AF"+last_key)
            last_ep = self.REF("EP"+last_key)
            # 上涨趋势，最高价大于前一个最高价，af就根据步长递增，否则保持
            if qushi:
                if(high>l_high):
                    af = last_af + S/100
                else:
                    af = last_af
                # af最大值
                if(af> M/100) : af = S/100
            else:
                # 下跌趋势，最低价小于前一个最低价，af就根据步长递增，否则保持
                if(low<l_low):
                    af = last_af + S/100
                else:
                    af = last_af
                # af最大值
                if(af> M/100) : af = S/100
            # sar 计算公式
            sar = last_sar + af*(last_ep - last_sar)
            # 这里计算的当前sar值也要进行拐点判断，我们规定sar不能触碰最低价最高价，否则反转
            if(qushi and low<=sar):
                ep = min_low
                sar = max_high
                af = 0
                qushi = not qushi

            elif(not qushi and high>=sar):
                # 如果下跌趋势当前的收盘价大于sar ，则表明进入反转上涨
                ep = max_high
                sar = min_low
                af = 0
                qushi = not qushi
    self.save_temp("AF"+last_key,af)
    self.save_temp("EP"+last_key,ep)
    self.save_temp("QS"+last_key,qushi)
    self.save_temp("SAR"+last_key,sar)
    return sar


def SARTURN(self:BaseSindexer,N:int,S:int,M:int):
    """抛物转向点
    用法:SARTURN(N,S,M),N为计算周期,S为步长,M为极值,若发生向上转向则返回1,若发生向下转向则返回-1,否则为0
    """
    SAR = self.SAR(N,S,M)
    if SAR==None:return 0
    last_key = ""+str(N)+"_"+str(S)+"_"+str(M)
    lSAR = self.REF("SAR"+last_key)
    lHIEG = self.REF("HIGH")
    lLOW = self.REF("LOW")
    HIGH = self.HIGH
    LOW = self.LOW
    if lSAR>0 and lSAR>=lHIEG and SAR<=LOW: 
        return 1
    if lSAR>0 and lSAR<=lLOW and SAR>=HIGH: 
        return -1
    return 0

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
    WINNER 函数主要是从图表上最左边的bar开始统计到当根bar，统计小于等于价格price的成交量与所有已经统计的bar的成交量之比。

    """

def ZIG(self:BaseSindexer,K:int,N:float):
    """之字转向 属于未来函数
    ZIG(K,N),当价格变化量超过N%时转向,K表示0:开盘价,1:最高价,2:最低价,3:收盘价
    ZIG(3,5)表示收盘价的5%的ZIG转向
    """
    zig = None
    # 计算过程缓存
    key = "zig_%s_%s_" % (K,N)
    CLOSE = "CLOSE"
    if K==0: CLOSE = "OPEN"
    if K==1: CLOSE = "HIGH"
    if K==2: CLOSE = "LOW"
    if K==3: CLOSE = "CLOSE"
    # 当前值
    value = self.GET(CLOSE)
    # 上一个低点
    zig_low = self.REF(key+"low")
    if not zig_low:zig_low = value
    # 上一个高点
    zig_high = self.REF(key+"high")
    if not zig_high:zig_high = value
    # 上一个低点位置
    zig_low_day = self.REF(key+"low_day")
    if zig_low_day==None:zig_low_day = self.cursor.index
    # 上一个高点位置
    zig_high_day = self.REF(key+"high_day")
    if zig_high_day==None:zig_high_day = self.cursor.index
    # 默认继承
    self.save_temp(key+"low",zig_low)
    self.save_temp(key+"high",zig_high)
    self.save_temp(key+"high_day",zig_high_day)
    self.save_temp(key+"low_day",zig_low_day)
    
    # 极点阀值，计算跟上一个低点的阀值
    fz = 100 * (value - zig_low) / zig_low
    # 如果极点阀值大于N，这个是高点
    if fz>=N:
        zig_max = self.HHV(CLOSE, self.cursor.index-zig_low_day);
        if value>=zig_max:
            # 更新中间的zig值
            self.__ZIG(CLOSE,zig_low_day,1)
            # 更新极点
            zig = value
            self.save_temp(key+"high",value)
            self.save_temp(key+"high_day",self.cursor.index)
        
    # 低点阀值
    fz = 100 * (value - zig_high) / zig_high
    if fz<=-N:
        zig_min = self.LLV(CLOSE, self.cursor.index-zig_high_day)
        if value<=zig_min:
            # 更新中间的zig值
            self.__ZIG(CLOSE,zig_high_day,0)
            # 更新极点
            zig = value
            self.save_temp(key+"low",value)
            self.save_temp(key+"low_day",self.cursor.index)

    # 最新一个k线值
    if(self.cursor.index==self.cursor.count-1):
        # 高点延续
        if zig_high_day>zig_low_day:
            # 更新中间的zig值
            self.__ZIG(CLOSE,zig_high_day,0)
            # 更新极点
            zig = value
            self.save_temp(key+"low",value)
            self.save_temp(key+"low_day",self.cursor.index)
        else:
            # 更新中间的zig值
            self.__ZIG(CLOSE,zig_low_day,1)
            # 更新极点
            zig = value
            self.save_temp(key+"high",value)
            self.save_temp(key+"high_day",self.cursor.index)
    
    return zig
       
    
def __ZIG(self:BaseSindexer,CLOSE,day,type=0):
    # 计算斜边长度
    first_value = self.GET(CLOSE,day)
    a = self.cursor.index - day
    b = first_value - self.GET(CLOSE)
    if(type>0):
        # 低到高
        b = self.GET(CLOSE) - first_value
    c = math.sqrt(a*a + b*b)
    # 计算b边长对向的角度,后面根据角度即可计算斜线c
    thetb = math.acos(a / c) * 180 / math.pi
    # 之前的低点位置全部为空
    for i in range(self.cursor.index-1,day,-1):
        a = i - day
        c = a / math.cos(thetb * math.pi / 180)
        b = first_value - math.sqrt(c ** 2 - a ** 2)
        if(type>0):
            b = first_value + math.sqrt(c ** 2 - a ** 2)
        # 更新之前的ZIG指标值
        subitem = self.klines[i]
        if hasattr(subitem,self.namespace):
            namespace = getattr(subitem,self.namespace)
            if namespace and self.variable_name:
                if hasattr(namespace,self.variable_name):
                    setattr(namespace,self.variable_name,b)
        


def ZIGA(self:BaseSindexer,K:int,N:float):
    """反向之字转向 属于未来函数
    用法:
    ZIGA(K,X),当价格变化超过X时转向,K表示0:开盘价,1:最高价,2:最低价,3:收盘价,其余:数组信息
    例如:
    ZIGA(3,1.5)表示收盘价变化1.5%的ZIGA转向
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