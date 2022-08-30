import connectors
import math

class Row():
    def __init__(self, start, a1, bolts):
        '''
        start: [x,y]... beginning of row
        a1: float ... distance between bolts in one row
        bolts: [*bolt]... list of objects of connectors.bolt clases
        '''
        self.start = start
        self.a1 = a1
        self.bolts = bolts
        self.edgeDistances()

    
    def edgeDistances(self):
        '''function that for each bolt in list of bolts adds edge min edge distances to EC
        '''
        for bolt in self.bolts:
            a1 = bolt.a1()
            a2 = bolt.a2()
            a3 = bolt.a3()
            a4t = bolt.a4t()
            a4c = bolt.a4c()
            
            distances = {
                "a1": a1,
                "a2": a2,
                "a3": a3,
                "a4t": a4t,
                "a4c": a4c
            }
            setattr(bolt, "distances", distances)
            
    def n(self):
        '''function that returns actual number of bolts in one row
        '''
        return len(self.bolts)
    
    def neff(self):
        '''function that returns number of effective bolts in one row
        '''
        n = self.n()
        n_eff = n**0.9 * (self.a1 / 13 / self.bolts[0].d) ** 0.25
        return min(n, n_eff)

class Member():
    '''class defining timber member
    
    t: thickness of member [mm]
    h: height of member [mm]
    '''
    
    def __init__(self,t,h):
        self.t = t
        self.h = h

class GroupOfBolts():
    '''class defining group of bolts in timber joint
    
    rows: [list] of Rows objects
    member: instance of Member class i.e. definition of timber member
    
    '''
    def __init__(self,rows,member):
        self.rows = rows
        self.member = member
        
    def checkA1(self):
        '''method checking min a1 distance of each row
        
        returns True if check OK otherwise False
        '''
        returnValue = True
        for row in self.rows:
            a1s = []
            for bolt in row.bolts:
                a1s.append(bolt.distances["a1"])
            maxA1 = max(a1s) #extracts maximum a1 distance from all bolts.
            
            if maxA1 >= row.a1:
                returnValue = False #default True value is switched to False once maximum a1 from each bolt is greater than actual a1 distances in model
        return returnValue
        
    def cehckA2(self):
        '''method checking min a2 distance of each row
        
        returns True if check OK otherwise False
        '''
        returnValue = True
 

bolts = []
for i in range(0,3):
    bolt = connectors.bolt(16,460,350,50*i,100)
    bolts.append(bolt)
    
row1 = Row([80,40],16*15,bolts)
row2 = Row([80,-40],16*7,bolts)

member = Member(120, 360)
group = GroupOfBolts([row1, row2], member)

group.checkA1()

