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
    
    @staticmethod
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
    
    @staticmethod
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

    @staticmethod
    def TRIX(X="CLOSE",N=12,M=9):
        s = """
        N:=%s;
        M:=%s;
        MTR:=EMA(EMA(EMA(%s,N),N),N);
        TRIX:(MTR-REF(MTR,1))/REF(MTR,1)*100;
        MATRIX:MA(TRIX,M);
        """ 
        return s % (N,M,X)

    @staticmethod
    def OBV(M=30):
        s = """
        M:=%s;
        VA:=IF(CLOSE>REF(CLOSE,1),VOL,-VOL);
        OBV:SUM(IF(CLOSE=REF(CLOSE,1),0,VA),0);
        MAOBV:MA(OBV,M);
        """
        return s % M
    
    @staticmethod
    def PSY(N=12,M=6):
        s = """
        N:=%s;
        M:=%s;
        PSY:COUNT(CLOSE>REF(CLOSE,1),N)/N*100;
        PSYMA:MA(PSY,M);
        """
        return s % (N,M)

    @staticmethod
    def BRAR(N=26):
        s = """
        N:=%s;
        BR:SUM(MAX(0,HIGH-REF(CLOSE,1)),N)/SUM(MAX(0,REF(CLOSE,1)-LOW),N)*100;
        AR:SUM(HIGH-OPEN,N)/SUM(OPEN-LOW,N)*100;
        """
        return s % N
    @staticmethod
    def ROC(N=12,M=6):
        s = """
        N:=%s;
        M:=%s;
        NN:=MIN(BARSCOUNT(C),N);
        ROC:100*(CLOSE-REF(CLOSE,NN))/REF(CLOSE,NN);
        MAROC:MA(ROC,M);
        """
        return s % (N,M)
    @staticmethod
    def CDP():
        s = """
        CH:=REF(H,1);
        CL:=REF(L,1);
        CC:=REF(C,1);
        CDP:(CH+CL+CC*2)/4;
        AH:CDP+CH-CL;
        NH:CDP+CDP-CL;
        NL:CDP+CDP-CH;
        AL:CDP-CH+CL;
        """
        return s
    @staticmethod
    def DMA(N1=10,N2=50,M=10):
        s = """
        N1:=%s;
        N2:=%s;
        M:=%s;
        DIF:MA(CLOSE,N1)-MA(CLOSE,N2);
        DIFMA:MA(DIF,M);
        """
        return s % (N1,N2,M)
    @staticmethod
    def CR(N=26,M1=10,M2=20,M3=40,M4=62):
        s = """
        N:=%s;
        M1:=%s;
        M2:=%s:
        M3:=%s;
        M4:=%s;
        MID:=REF(HIGH+LOW,1)/2;
        CR:SUM(MAX(0,HIGH-MID),N)/SUM(MAX(0,MID-LOW),N)*100;
        MA1:REF(MA(CR,M1),M1/2.5+1);
        MA2:REF(MA(CR,M2),M2/2.5+1);
        MA3:REF(MA(CR,M3),M3/2.5+1);
        MA4:REF(MA(CR,M4),M4/2.5+1);
        """
        return s % (N,M1,M2,M3,M4)
    @staticmethod
    def EMV(N=14,M=9):
        s = """
        N:=%s;
        M:=%s;
        VOLUME:=MA(VOL,N)/VOL;
        MID:=100*(HIGH+LOW-REF(HIGH+LOW,1))/(HIGH+LOW);
        EMV:MA(MID*VOLUME*(HIGH-LOW)/MA(HIGH-LOW,N),N);
        MAEMV:MA(EMV,M);
        """
        return s % (N,M)
    @staticmethod
    def MIKE(N=10):
        s = """
        N:=%s;
        HLC:=REF(MA((HIGH+LOW+CLOSE)/3,N),1);
        HV:=EMA(HHV(HIGH,N),3);
        LV:=EMA(LLV(LOW,N),3);
        STOR:EMA(2*HV-LV,3);
        MIDR:EMA(HLC+HV-LV,3);
        WEKR:EMA(HLC*2-LV,3);
        WEKS:EMA(HLC*2-HV,3);
        MIDS:EMA(HLC-HV+LV,3);
        STOS:EMA(2*LV-HV,3);
        """
        return s % N
    @staticmethod
    def EXPMA(M1=12,M2=50):
        s = """
        M1:=%s;
        M2:=%s;
        EXP1:EMA(CLOSE,M1);
        EXP2:EMA(CLOSE,M2);
        """
        return s % (M1,M2)
    @staticmethod
    def VR(N=26,M=6):
        s = """
        N:=%s;
        M:=%s;
        TH:=SUM(IF(CLOSE>REF(CLOSE,1),VOL,0),N);
        TL:=SUM(IF(CLOSE<REF(CLOSE,1),VOL,0),N);
        TQ:=SUM(IF(CLOSE=REF(CLOSE,1),VOL,0),N);
        VR:100*(TH*2+TQ)/(TL*2+TQ);
        MAVR:MA(VR,M);
        """
        return s % (N,M)
    @staticmethod
    def WVAD(N=24,M=6):
        s = """
        N:=%s;
        M:=%s;
        WVAD:SUM((CLOSE-OPEN)/(HIGH-LOW)*VOL,N)/10000;
        MAWVAD:MA(WVAD,M);
        """
        return s % (N,M)
    


