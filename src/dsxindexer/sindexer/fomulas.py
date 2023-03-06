class Formulas:

    @staticmethod
    def MACD(X="CLOSE",SHORT=12,LONG=26,MID=9): 
        s = """
        SHORT:=%s;
        LONG:=%s;
        MID:=%s;
        DIF:=EMA(%s,SHORT)-EMA(%s,LONG);
        DEA:=EMA(DIF,MID);
        MACD:=(DIF-DEA)*2;
        """
        return s % (SHORT,LONG,MID,X,X)
    
    @staticmethod
    def KDJ(X="CLOSE",N=9,M1=3,M2=3): 
        s = """
        N:=%(N)s; M1:=%(M1)s; M2:=%(M2)s;
        RSV:=(%(X)s-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100;
        K:=SMA(RSV,M1,1);
        D:=SMA(K,M2,1);
        J:=3*K-2*D;
        """
        return s % {"N":N,"M1":M1,"M2":M2,"X":X}
