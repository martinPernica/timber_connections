class timber2():
    '''class that calculates characteristic shear resistance of timber-timber connections
    
    accepts as arguments couple of objects type "bolt" or "nail"
    '''
    def __init__(self, ply1, ply2):
        self.d = ply1.d
        self.beta = ply2.fhk() / ply1.fhk()
        self.t1 = ply1.t
        self.t2 = ply2.t
        self.fhk1 = ply1.fhk()
        self.fhk2 = ply2.fhk()
        self.Myrk = ply1.MyRk()
    
    def FvrkA(self):
        '''method that calculates Fvrk to 8.6(a)
        '''
        Fvrk = self.fhk1 * self.t1 * self.d
        return Fvrk
    
    def FvrkB(self):
        '''methd that calculates Fvrk to 8.6(b)
        '''
        Fvrk = self.fhk2 * self.t2 * self.d
        return Fvrk
    
    def FvrkC(self):
        '''method that calculates Fvrk to 8.6(c)
        '''
        p1 = self.fhk1 * self.t1 * self.d / (1 + self.beta)
        p2 = (self.beta + 2 * self.beta**2 * (1 + self.t2 / self.t1 + (self.t2 / self.t1) ** 2) +   self.beta**3* (self.t2 / self.t1)**2)**0.5
        p3 = self.beta * (1+self.t2 / self.t1)
        Fvrk = p1 * (p2 - p3)
        return Fvrk
    
    def FvrkD(self):
        '''method that calculates Fvrk to 8.6(d)
        '''
        p1 = 1.05 * self.fhk1 * self.t1 * self.d / (2 + self.beta)
        p2 = (2 * self.beta * (1 + self.beta) + (4 * self.beta * (2 + self.beta) * self.Myrk)/(self.fhk1 *self.d*self.t1**2))**0.5
        Fvrk = p1 * (p2 - self.beta)
        return Fvrk
    
    def FvrkE(self):
        '''method that calculates Fvrk to 8.6(e)
        '''
        p1 = 1.05 * self.fhk1 * self.t2 * self.d / (1 + 2 * self.beta)
        p2 = (2 * self.beta** 2 * (1 + self.beta) + (4 * self.beta * (1 + 2 * self.beta) * self.Myrk)/(self.fhk1 *self.d*self.t2**2))**0.5
        Fvrk = p1 * (p2 - self.beta)
        return Fvrk
    
    def FvrkF(self):
        '''method that calculates Fvrk to 8.6(f)
        '''
        Fvrk = 1.15 * (2*self.beta / (1 + self.beta))**0.5 * (2 * self.Myrk * self.fhk1 * self.d) ** 0.5
        return Fvrk
    
    def Fvrk(self):
        '''method that returns characteristic shear resistance for the connections
        '''
        return min(self.FvrkA(), self.FvrkB(), self.FvrkC(), self.FvrkD(), self.FvrkE(), self.FvrkF())

class timber3():

    '''class that calculates characteristic shear resistance of timber-timber-timber connections
    
    accepts as arguments couple of objects type "bolt" or "nail"
    ply1: outer ply
    ply2: inner ply
    '''

    def __init__(self, ply1, ply2):
        self.d = ply1.d
        self.beta = ply2.fhk() / ply1.fhk()
        self.t1 = ply1.t
        self.t2 = ply2.t
        self.fhk1 = ply1.fhk()
        self.fhk2 = ply2.fhk()
        self.Myrk = ply1.MyRk()
        
    def FvrkG(self):
        Fvrk = self.fhk1 * self.t1 * self.d
        return 2 * Fvrk
        
    def FvrkH(self):
        Fvrk = 0.5 * self.fhk2 * self.t2 * self.d
        return 2 * Fvrk
        
    def FvrkJ(self):
        p1 = 1.05 * self.fhk1 * self.t1 * self.d / (2 + self.beta)
        p2 = (2 * self.beta * (1 + self.beta) + 4 * self.beta * (2 + self.beta) * self.Myrk / (self.fhk1 * self.d * self.t1 ** 2))**0.5
        Fvrk = p1 * (p2 - self.beta)
        return 2 * Fvrk
        
    def  FvrkK(self):
        Fvrk = 1.15 * (2 * self.beta / (1 + self.beta))**0.5 * (2 * self.Myrk * self.fhk1 * self.d) ** 0.5
        return 2 * Fvrk
            
    def Fvrk(self):
        return min(self.FvrkG(), self.FvrkH(), self.FvrkJ(), self.FvrkK())
 

class timberPlate():
    '''class that calculates shear resistance of timber to plate connection.
    
    ply1 is an instance of bolt class, tp is thickness of the plate'''
    def __init__(self, ply1, tp = 0):
        self.d = float(ply1.d)
        self.t1 = float(ply1.t)
        self.fhk1 = ply1.fhk()
        self.Myrk = ply1.MyRk()
        if tp != 0: #this is for a backward compability
            self.tp = float(tp)
        else:
            ply1.tp = ply1.tp
    
    def FvrkA(self):
        Fvrk = 0.4 * self.fhk1 * self.t1 * self.d
        return Fvrk
    
    def FvrkB(self):
        Fvrk = 1.15 * (2 * self.Myrk * self.fhk1 * self.d) ** 0.5
        return Fvrk
     
    def FvrkC(self):
        Fvrk = self.t1 * self.fhk1 * self.d
        return Fvrk
        
    def FvrkD(self):
        p1 = self.fhk1 * self.t1 * self.d
        p2 = ((2 + 4 * self.Myrk / (self.fhk1 * self.d * self.t1 ** 2))**0.5) - 1
        Fvrk = p1 * p2
        return Fvrk
    
    def FvrkE(self):
        Fvrk = 2.3 * (self.Myrk * self.fhk1 * self.d)**0.5
        return Fvrk
        
    def Fvrk(self):
        if self.tp <= self.d * 0.5:
            return min(self.FvrkA(), self.FvrkB())
        elif self.tp >= self.d:
            return min(self.FvrkC(), self.FvrkD(), self.FvrkE())
        else:
            FvrkThin = min(self.FvrkA(), self.FvrkB())
            FvrkThick = min(self.FvrkC(), self.FvrkD(), self.FvrkE())
            deltaP = self.tp - self.d * 0.5
            deltaF = FvrkThick - FvrkThin
            Fvrk = FvrkThin + deltaF / (0.5*self.d) * deltaP
            return Fvrk

class timberPlateTimber():

    def __init__(self, ply1, tp = 0):
        self.d = float(ply1.d)
        self.t1 = float(ply1.t)
        self.fhk1 = ply1.fhk()
        self.Myrk = ply1.MyRk()
        if tp != 0: #this is for a backward compability
            self.tp = float(tp)
        else:
            ply1.tp = ply1.tp
    
    def FvrkF(self):
        Fvrk = self.fhk1 * self.t1 * self.d
        return 2 * Fvrk
    
    def FvrkG(self):
        p1 = self.fhk1 * self.t1 * self.d
        p2 = (2 + (4 * self.Myrk) / (self.fhk1 * self.d * self.t1 **2)) ** 0.5
        Fvrk = p1 * p2
        return 2 * Fvrk
    
    def FvrkH(self):
        Fvrk = 2.3 * (self.Myrk * self.fhk1 * self.d) ** 0.5
        return 2 * Fvrk
    
    def Fvrk(self):
        return min(self.FvrkF(), self.FvrkG(), self.FvrkH())
        
class plateTimberPlate():

    def __init__(self, ply1, tp = 0):
        self.d = float(ply1.d)
        self.t2 = float(ply1.t)
        self.fhk2 = ply1.fhk()
        self.Myrk = ply1.MyRk()
        if tp != 0: #this is for a backward compability
            self.tp = float(tp)
        else:
            ply1.tp = ply1.tp
        
    def FvrkJ(self):
        Fvrk = 0.5 * self.fhk2 * self.t2 * self.d
        return 2 * Fvrk
        
    def FvrkK(self):
        Fvrk = 1.15*(2 * self.Myrk * self.fhk2 * self.d) ** 0.5
        return 2 * Fvrk
    
    def FvrkL(self):
        Fvrk = 0.5 * self.fhk2 * self.t2 *self.d
        return 2 * Fvrk
    
    def FvrkM(self):
        Fvrk = 2.3 * (self.Myrk * self.fhk2 * self.d) ** 0.5
        return 2 * Fvrk
    
    def Fvrk(self):
        if self.tp <= self.d * 0.5:
            return min(self.FvrkJ(), self.FvrkK())
        elif self.tp >= self.d:
            return min(self.FvrkL(), self.FvrkM())
        else:
            FvrkThin = min(self.FvrkJ(), self.FvrkK())
            FvrkThick = min(self.FvrkL(), self.FvrkM())
            deltaP = self.tp - self.d * 0.5
            deltaF = FvrkThick - FvrkThin
            Fvrk = FvrkThin + deltaF / (0.5 * self.d) * deltaP
            return Fvrk