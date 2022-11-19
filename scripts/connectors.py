import math

class bolt():
    def __init__(self, d, fu, ro, alfa, t, tp = 0, woodType = "softWood", board = "No", roM = 400):
        '''woodTypes: Board, Softwood, LVL, Hardwood. Not important for boards
        board: No, plywood, OSB
        t = thickness of timber
        tpl = thickness of plate if any
        '''
        self.d = float(d)
        self.fu = float(fu)
        self.ro = float(ro)
        self.alfa = float(alfa) #angle in degrees
        self.woodType = woodType
        self.board = board
        self.t = float(t)
        self.tp = float(tp)
        self.roM = roM
    
    def MyRk(self):
        '''method that calculates characteristic yield moment
        '''
        return 0.3 * self.fu * self.d ** 2.6
    
    def fhk(self):
        '''method that calculates characteristic embedment strength
        '''
        if self.board == "No":
            fh0k = 0.082*(1-0.01 * self.d) * self.ro
            if self.woodType == "softWood" or self.WoodType == "glulam":
                k90 = 1.35 + 0.015 * self.d
            elif self.woodType == "LVL":
                k90 = 1.30 + 0.015 * self.d
            else:
                k90 = 0.90 + 0.015 * self.d
            alfa = self.alfa / 180 * math.pi
            fhk = fh0k / (k90 * math.sin(alfa)**2 + math.cos(alfa)**2)
            return fhk
        elif sekf.board == "plywood":
            fhk = 0.11*(1-0.01 * self.d) * self.ro
            return fhk
        #following is for OSB board
        else:
            fhk = 50 * self.d **(-0.6) * t**0.2
            return fhk
    
    def a1(self):
        '''method that calculates min a1 distance of the bolt 
        
        returns value in [mm]
        '''
        return (4 + abs(math.cos(self.alfa))) * self.d
    
    def a2(self):
        '''method that calculates min a2 distance of the bolt 
        
        returns value in [mm]
        '''
        return 4 * self.d
        
    def a3(self):
        '''method that returns min a3 loaded or unloaded edge distance. 
        
        Whether its loaded or unloaded depends on the angle alfa
        returns value in [mm]
        '''
        alfa = self.alfa / 180 * math.pi
        
        if self.alfa <= 90 or self.alfa >= 270:
            return max(7 * self.d, 80)
        
        elif self.alfa > 90 and self.alfa <150:
            return (1 + 6 * math.sin(alfa)) * self.d
            
        elif self.alfa >= 150 and self.alfa < 210:
            return 4 * self.d
            
        else:
            return (1 + 6 * math.sin(alfa)) * self.d
            
    def a4t(self):
        '''method that returns min a4 distance to loaded edge. 
        
        returns value in [mm]
        '''
        alfa = self.alfa / 180 * math.pi
        
        return max((2 + 2 * math.sin(alfa)) * self.d, 3 * self.d) 
        
    def a4c(self):
        '''method that returns min a4 distance to UNloaded edge. 
        
        returns value in [mm]
        '''
        
        return 3 * self.d
        
    def kSer(self):
        '''method returning serviceability slip moduli
        '''
        return self.roM ** 1.5 * self.d / 23

        
    
        
    
    
            
    