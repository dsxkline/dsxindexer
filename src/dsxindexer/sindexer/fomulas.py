class Formulas:

    @staticmethod
    def MACD(X="CLOSE",SHORT=12,LONG=26,MID=9): 
        s = """
        SHORT:=%s;
        LONG:=%s;
        MID:=%s;
        DIF:EMA(%s,SHORT)-EMA(%s,LONG);
        DEA:EMA(DIF,MID);
        MACD:(DIF-DEA)*2;
        """
        return s % (SHORT,LONG,MID,X,X)
    
    @staticmethod
    def KDJ(X="CLOSE",N=9,M1=3,M2=3): 
        s = """
        N:=%(N)s; M1:=%(M1)s; M2:=%(M2)s;
        RSV:=(%(X)s-LLV(LOW,N))/(HHV(HIGH,N)-LLV(LOW,N))*100;
        K:SMA(RSV,M1,1);
        D:SMA(K,M2,1);
        J:3*K-2*D;
        """
        return s % {"N":N,"M1":M1,"M2":M2,"X":X}

    @staticmethod
    def RSI(X="CLOSE",N1=6,N2=12,N3=24):
        s = """
        N1:=%(N1)s;
        N2:=%(N2)s;
        N3:=%(N3)s;
        LC:=REF(%(X)s,1);
        RSI1:SMA(MAX(%(X)s-LC,0),N1,1)/SMA(ABS(%(X)s-LC),N1,1)*100;
        RSI2:SMA(MAX(%(X)s-LC,0),N2,1)/SMA(ABS(%(X)s-LC),N2,1)*100;
        RSI3:SMA(MAX(%(X)s-LC,0),N3,1)/SMA(ABS(%(X)s-LC),N3,1)*100;
        """
        return s % {"X":X,"N1":N1,"N2":N2,"N3":N3}
    
    @staticmethod
    def CCI(N=14):
        s = """
        TYP:=(HIGH+LOW+CLOSE)/3;
        CCI%s:(TYP-MA(TYP,%s))*1000/(15*AVEDEV(TYP,%s));
        """
        return s % (N,N,N)
    
    @staticmethod
    def WR(N=10,N1=6):
        s = """
        N:=%s;
        N1:=%s;
        WR%s:100*(HHV(HIGH,N)-CLOSE)/(HHV(HIGH,N)-LLV(LOW,N));
        WR%s:100*(HHV(HIGH,N1)-CLOSE)/(HHV(HIGH,N1)-LLV(LOW,N1));
        """ 
        return s % (N,N1,N,N1)
    
    def DMI(N=14,M=6):
        s = """
        N:=%s;
        M:=%s;
        MTR:=SUM(MAX(MAX(HIGH-LOW,ABS(HIGH-REF(CLOSE,1))),ABS(REF(CLOSE,1)-LOW)),N);
        HD :=HIGH-REF(HIGH,1);
        LD :=REF(LOW,1)-LOW;
        DMP:=SUM(IF(HD>0&&HD>LD,HD,0),N);
        DMM:=SUM(IF(LD>0&&LD>HD,LD,0),N);
        PDI: DMP*100/MTR;
        MDI: DMM*100/MTR;
        ADX: MA(ABS(MDI-PDI)/(MDI+PDI)*100,M);
        ADXR:(ADX+REF(ADX,M))/2;
        """
        return s % (N,M)
    
    def BOLL(X="CLOSE",M=20,K=2):
        s = """
        M:=%s;
        K:=%s;
        MB:=MA(%s,M);
        STD:=STD(%s,M);
        MID:MB;
        UP:MB+K*STD;
        LOW:MB-K*STD;
        """
        return s % (M,K,X,X)


