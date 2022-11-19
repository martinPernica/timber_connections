import math
import os
import sys
import copy

current_dir = os.path.dirname(os.path.realpath(__file__))
parrent_dir = os.path.dirname(current_dir)
scripts_dir = os.path.join(parrent_dir, "scripts")
sys.path.append(scripts_dir)

import connectors
import timberShearJoints as joints


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
        self.boltCoordinates()
        self.charResistance()
        #self.printBoltCoordinates()

    
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
            
    def boltCoordinates(self):
        '''method adding [x,y] coordinate to each bolt
        '''
        a1Tot = 0
        for bolt in self.bolts:
            x = self.start[0] + a1Tot
            y = self.start[1]
            a1Tot += self.a1
            coordinates = [x, y]
            #print("coordinates {}".format(coordinates))
            setattr(bolt, "coordinates", coordinates)
            #print("saved coordinates: {}".format(bolt.coordinates))           
            
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
    
    def printBoltCoordinates(self):
        for bolt in self.bolts:
            print("X = {}, Y = {}".format(bolt.coordinates[0], bolt.coordinates[1]))
            
    def charResistance0(self, joint = "timberPlatetTimber"):
        '''method adding F_v,Rk to each bolt
        '''
        for bolt in self.bolts:
            nred = self.neff() / self.n()
            alfa = bolt.alfa # in degree
            #calculate char shear resistance for alfa = 0
            Fvrk0 = 0
            bolt.alfa = 0
            if joint == "timber2":
                pass
            elif joint == "timber3":
                pass
            elif joint == "timberPlate":
                Fvrk0 = joints.timberPlate(bolt).Fvrk()
            elif joint == "timberPlatetTimber":
                Fvrk0 = joints.timberPlateTimber(bolt).Fvrk()
            elif joint == "plateTimberPlate":
                Fvrk0 = joints.plateTimberPlate(bolt).Fvrk()
            #print("Fvrk0 = {}".format(Fvrk0)) 
            bolt.alfa = alfa #return original value of the alfa
            setattr(bolt, "Fvrk0",Fvrk0)

    def charResistance90(self, joint = "timberPlateTimber"):
        for bolt in self.bolts:
            alfa = bolt.alfa
            #calculata char shear resistance fo alfa = 90
            Fvrk90 = 0            
            bolt.alfa = 90  
            if joint == "timber2":
                pass
            elif joint == "timber3":
                pass
            elif joint == "timberPlate":
                Fvrk90 = joints.timberPlate(bolt).Fvrk()
            elif joint == "timberPlatetTimber":
                Fvrk90 = joints.timberPlateTimber(bolt).Fvrk()
            elif joint == "plateTimberPlate":
                Fvrk90 = joints.plateTimberPlate(bolt).Fvrk()
            bolt.alfa = alfa #return original value of the alfa
            setattr(bolt, "Fvrk90",Fvrk90)
                
    def charResistance(self, joint = "timberPlateTimber"):
        '''calculate interpolated value between Fvrk and Fvrk 90
        '''
        self.charResistance0(joint = joint)
        self.charResistance90(joint = joint)
        
        nred = self.neff() / self.n()
        
        for bolt in self.bolts:        
            #calculate interpolated value
            alfa = bolt.alfa #return the original value
            ns = int(alfa/90)
            alfaRed = alfa - ns * 90 #calculates angle between 0 and 90 
            Fvrk = 0
            Fvrk0 = bolt.Fvrk0
            Fvrk90 = bolt.Fvrk90
            
            if Fvrk0 >= Fvrk90:
                Fvrk = Fvrk90 + (Fvrk0 - Fvrk90) * (90 - alfaRed) / 90
            else:
                Fvrk = Fvrk0 + (Fvrk90 - Fvrk0) * alfaRed / 90
            setattr(bolt, "Fvrk", Fvrk)
    
    def changeBoltsDiameter(self, d):
        for bolt in self.bolts:
            bolt.d = d
    
    def changeBoltsFu(self,fu):
        for bolt in self.bolts:
            bolt.fu = fu
            
    def changeTimberThicnkess(self, t):
        for bolt in self.bolts:
            bolt.t = t
    
    def changeTimberDensity(self, ro):
        for bolt in self.bolts:
            bolt.ro = ro
    
    def changePlateThickness(self, tp):
        for bolt in self.bolts:
            bolt.tp = tp
            
    def changeNoBolts(self, No):
        '''method that chenges no of bolts in one row
        
        all bolts have to be of the same specificatio i.e. material, diameter etc.
        '''
        nActulal = len(self.bolts)
        bolt = copy.deepcopy(self.bolts[0])
        
        while True:
            if No < nActual:
                self.bolts.pop()
            else:
                break
        
        while True:
            if No > nActual:
                self.bolts.append(bolt)
            else:
                break
    
    def changeA1(self, a1):
        self.a1 = a1
    
    def changeStart(self, start):
        self.start = start

class Member():
    '''class defining timber member
    
    t: thickness of member [mm]
    h: height of member [mm]
    beta: angle of chamfer [degree]
    '''
    
    def __init__(self,t,h,beta=0, ro = 350, roM = 400, tp = 0):
        self.t = t
        self.h = h
        self.beta = beta
        self.ro = ro
        self.roM = roM
        self.tp = tp
    
    def changeT(self, t):
        self.t = t
    
    def changeH(self, h):
        self.h = h
    
    def changeBeta(self, beta):
        self.beta = beta
    
    def changeRo(self, ro):
        self.ro = ro
        
    def changeRoM(self, roM):
        self.roM = roM
    
    def changeTp(self, tp):
        self.tp = tp

class GroupOfBolts():
    '''class defining group of bolts in timber joint
    
    rows: [list] of Rows objects
    member: instance of Member class i.e. definition of timber member
    
    '''
    def __init__(self,rows,member):
        self.rows = rows
        self.member = member
        self.noOfRows = len(rows)
        self.topEdgeY = member.h / 2
        self.bottomEdgeY = - member.h / 2
        self.rowNumbering()
        
    def rowNumbering(self):
        '''sets row number to each row
        '''
        i = 1
        for row in self.rows:
            setattr(row, "no", i)
            i += 1
            
    def deleteRow(self, no):
        '''delete row with a "no" number and reruns numbering of all rows
        '''
        for row in self.rows:
            if row.no == no:
                self.rows.remove(row)
        self.rowNumbering()
     
    def addRow(self,row):
        '''adds row and runs renumbering of all rows
        
        row has to be an instance of the groupOfBolts.row class
        '''
        self.rows.append(row)
        self.rowNumbering()
        
    def checkA1(self):
        '''method checking min a1 distance of each row
        
        returns True if check OK otherwise False
        '''
        returnValue = True
        for row in self.rows:
            a1s = []
            for bolt in row.bolts:
                a1s.append(bolt.distances["a1"])
            minA1 = max(a1s) #extracts maximum a1 distance from all bolts.
            
            if minA1 >= row.a1:
                returnValue = False #default True value is switched to False once maximum a1 from each bolt is greater than actual a1 distances in model
        
        return returnValue
        
    def checkA2(self):
        '''method checking min a2 distance of each row
        
        returns True if check OK otherwise False
        '''
        returnValue = True
        for i in range(0, self.noOfRows):
            minA2 = self.rows[i].bolts[0].distances["a2"] #min a2 is the same for all bolts provided they have the same diamteter... which I assume they will have
            yi = self.rows[i].start[1] #get y coordinate of the beginning of row
            for j in range(0, self.noOfRows):
                if i == j:
                    continue
                    print("passing")
                yj = self.rows[j].start[1]
                distance = abs(yi - yj)
                print("distance between row {} and {} is {} mm".format(i,j,distance))
                if distance <= minA2:
                    returnValue = False #swithc returnValue to false if a2 is not satisfactory
                    print("distance is not satisfactory")
                    
        return returnValue
        
    def checkA3(self):
        '''method checking min a3 distance of first bolt in row
        
        returns True if check OK otherwise False
        '''
        beta = self.member.beta/180 * math.pi
        returnValue = True
        for row in self.rows:
            minA3 = row.bolts[0].distances["a3"]
            x = row.start[0]
            y = row.start[1]
            #calculate X coordinate of intersection betweel center line of row and the end of timber
            xEdge = y * math.tan(beta)
            #distance between end of member and edge end of row
            a3 = x - xEdge
            print("end distance a3 is {} mm, minimum distance a3 is {} mm".format(a3, minA3))
            if minA3 > a3:
                print("distance a3 is not satisfactory")
                returnValue = False
                
        return returnValue
    
    def checkA4(self):
        '''method checking min a4 distance of each BOLT
        
        returns True if check OK otherwise False
        '''
        returnValue = True
        for row in self.rows:
            rowNo = self.rows.index(row)
            y = row.start[1]
            toTop = self.member.h / 2 - y
            toBottom = self.member.h / 2 + y
            print("row no {} to TOP {} mm to BOTTOM {} mm".format(rowNo, toTop, toBottom))
                        
            for bolt in row.bolts:
                boltNo = row.bolts.index(bolt)
                print("row no {} - bolt no {} - alfa  {} degree".format(rowNo, boltNo,bolt.alfa))
                
                minA4t = bolt.distances["a4t"]
                minA4c = bolt.distances["a4c"]
                alfa = bolt.alfa / 180 * math.pi
                
                if alfa <= math.pi:
                    if minA4t > toBottom:
                        returnValue = False
                        print("BOTTOM edge is loaded, min a4t {} mm is NOT OK".format(minA4t))
                    else:
                        print("BOTTOM edge is loaded, min a4t {} mm is OK".format(minA4t))
                    
                    if minA4c > toTop:
                        returnValue = False
                        print("TOP edge is NOTloaded, min a4c {} mm is NOT OK".format(minA4c))
                    else:
                        print("TOP edge is NOTloaded, min a4c {} mm is OK".format(minA4c))
                
                else:
                    if minA4t > toTop:
                        returnValue = False 
                        print("BOTTOM edge is NOTloaded, min a4c {} mm is NOT OK".format(minA4c))
                    else:
                        print("BOTTOM edge is NOTloaded, min a4c {} mm is OK".format(minA4c))
                    
                    if minA4c > toBottom:
                        returnValue = False
                        print("TOP edge is loaded, min a4t {} mm is NOT OK".format(minA4t))
                    else:
                        print("TOP edge is loaded, min a4t {} mm is OK".format(minA4t))
        
        return returnValue
        
    def printBoltCoordinates(self):
        i = 0
        for row in self.rows:
            j = 0
            for bolt in row.bolts:
                print("row {} - bolt {}: x = {}, y = {}".format(i,j,bolt.coordinates[0],bolt.coordinates[1]))
                j += 1
            i += 1  

    def designShearResistance(self, gammaM = 1, kmod = 1, toPrint = False):
        '''returns design shear resistance for each bolt
        
            if toPrin = True values will be printed
        '''
        returnValue = {}
        for row in self.rows:
            #update characteristic resistances of each bolt to actual input
            row.charResistance0()
            row.charResistance90()
            row.charResistance()
            no = row.no
            returnValue[no] = None
            j = 0
            vals = []
            for bolt in row.bolts:
                vals.append(kmod * bolt.Fvrk / gammaM)
            returnValue[no] = vals
        if toPrint:
            print(returnValue)
            
        return returnValue
    
    def changeT(self, t):
        '''Changes "t" ie thickness paramater for each bolt in each row
        '''
        for row in self.rows:
            for bolt in row.bolts:
                bolt.t = t
    
    def changeTp(self, tp):
        '''Changes "tp" ie thickness of plate for each bolt in each row
        '''
        for row in self.rows:
            for bolt in row.bolts:
                bolt.tp = tp
    
    def ctrStifness(self):
        '''Calculates and returns coordinates of ctr of rotation
        
        returns [] where [0] is X coordinate of ctro of stifness resp. [1] is Y coordinate
        '''
        product = []
        for row in self.rows:
            for bolt in row.bolts:
                kSer = bolt.kSer()
                XkSer = bolt.coordinates[0] * kSer
                YkSer = bolt.coordinates[1] * kSer
                product.append([kSer, XkSer, YkSer])
        stiff = 0
        stiffX = 0
        stiffY = 0
        for prod in product:
            stiff += prod[0]
            stiffX += prod[1]
            stiffY += prod[2]
        x = stiffX / stiff
        y = stiffY / stiff
        
        return [x,y]
                
            
                          

'''bolts = []
for i in range(0,3):
    bolt = connectors.bolt(16,460,350,50*i,100)
    bolts.append(bolt)
    
row1 = Row([80,140],16*15,bolts)
row2 = Row([80,-140],16*7,bolts)
row3 = Row([80,0],16*7,bolts)

member = Member(120, 360, 35)
group = GroupOfBolts([row1, row2, row3], member)

print("__CHECK OF A1__")
group.checkA1()
print("__CHECK OF A2__")
group.checkA2()
print("__CHECK OF A3__")
group.checkA3()
print("__CHECK OF A4__")
group.checkA4()'''



