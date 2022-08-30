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
        
        
    

bolts = []
for i in range(0,3):
    print(i)
    bolt = connectors.bolt(16,460,350,50*i,100)
    bolts.append(bolt)
    
row1 = Row([80,40],16*15,bolts)
for bolt in row1.bolts:
    print(bolt.distances)
print(row1.n())
print(row1.neff())

row2 = Row([80,-40],16*7,bolts)

