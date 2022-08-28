import math

class bolt():
    def __init__(self, d, fu, ro, alfa, t, woodType = "softWood", board = "No"):
        '''woodTypes: Board, Softwood, LVL, Hardwood. Not important for boards
        board: No, plywood, OSB
        t = thickness
        '''
        self.d = float(d)
        self.fu = float(fu)
        self.ro = float(ro)
        self.alfa = float(alfa)
        self.woodType = woodType
        self.board = board
        self.t = float(t)
    
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