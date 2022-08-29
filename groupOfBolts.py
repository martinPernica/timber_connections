import connectors



class Row():
    def __init__(self, start, a1, bolts):
    '''
    start: [x,y]... beginning of row
    a1: float ... distance between bolts in one row
    bolts: [*bolt]... list of objects of connectors.bolt clases
    '''
    self.start = start
    self.bolts = bolts
    
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