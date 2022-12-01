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
            if hasattr(bolt, "distances"):
                bolt.distances = distances
            else:
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
            setattr(bolt, "coordinates", coordinates)          
            
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
            
    def charResistance0(self, joint = "timberPlateTimber"):
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
            elif joint == "timberPlateTimber":
                Fvrk0 = joints.timberPlateTimber(bolt).Fvrk()
            elif joint == "plateTimberPlate":
                Fvrk0 = joints.plateTimberPlate(bolt).Fvrk()
            #print("Fvrk0 = {}".format(Fvrk0)) 
            bolt.alfa = alfa #return original value of the alfa
            if hasattr(bolt, "Fvrk0"):
                bolt.Fvrk0 = Fvrk0
            else:
                setattr(bolt, "Fvrk0",Fvrk0)
            #print("char resistance0 is {}".format(Fvrk0))

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
            elif joint == "timberPlateTimber":
                Fvrk90 = joints.timberPlateTimber(bolt).Fvrk()
            elif joint == "plateTimberPlate":
                Fvrk90 = joints.plateTimberPlate(bolt).Fvrk()
            bolt.alfa = alfa #return original value of the alfa
            if hasattr(bolt, "Fvrk90"):
                bolt.Fvrk90 = Fvrk90
            else:
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
            #calculates angle between 0 and 90
            if alfa <= 90:
                alfaRed = alfa
            elif alfa > 90 and alfa <= 180:
                alfaRed = 180 - alfa
            elif alfa >180 and alfa <= 270:
                alfaRed = alfa - 180
            else:
                alfaRed = 270 - alfa
            Fvrk = 0
            Fvrk0 = bolt.Fvrk0
            Fvrk90 = bolt.Fvrk90
            
            if Fvrk0 >= Fvrk90:
                Fvrk = Fvrk90 + (Fvrk0 * nred - Fvrk90) * (90 - alfaRed) / 90
            else:
                Fvrk = Fvrk0 * nred + (Fvrk90 - Fvrk0 * nred) * alfaRed / 90
            if hasattr(bolt, "Fvrk"):
                bolt.Fvrk = Fvrk
            else:
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
        self.warningEdge = "svorník {no}: {a} = {aVal} mm < {amin} = {aminVal} mm -> NEVYHOVUJE"
        
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
        
        returns returnValue = [varning message 1, varning message 2, ...]
        '''
        print("Checking A1")
        returnValue = []
        print(self.rows)
        for row in self.rows:
            print("Iam here1")
            a1 = row.a1
            rowNo = row.no
            i = 1
            print("rownNo = {}".format(rowNo))
            for bolt in row.bolts:
                a1min = round(bolt.a1()*10)/10
                print("min distance {} - {} = {}".format(rowNo, i, a1min))
                if a1 <= a1min:
                    num = "{}-{}".format(rowNo,i)
                    #"svorník {no}: {a} = {aVal} mm < {amin} = {aminVal} mm -> NEVYHOVUJE"
                    print(self.warningEdge)
                    string = self.warningEdge.format(no = num, a = "a1", aVal = a1, amin = "a1min", aminVal = a1min)
                    print(string)
                    returnValue.append(string)
                i += 1        
        
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
        
    def checkDistances(self):
        '''method wrapping all distance checks
        
        returns returnValue = [warning message 1, warning message 2]
        '''
        returnValue = []

        a1 = self.checkA1()
        try:
            for message in a1:
                returnValue.append(message)
        except:
            pass
        
        if len(returnValue) == 0:
            return ["VZDÁLENOSTI SVORNÍKŮ V POŘÁDKŮ"]
        else:
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
        '''adds design shear resistance to each bolt
        '''
        returnValue = {}
        for row in self.rows:
            #update characteristic resistances of each bolt to actual input
            row.charResistance()
            n = row.n()
            neff = row
            for bolt in row.bolts:
                Fvrd = kmod * bolt.Fvrk / gammaM

 
    
    def changeT(self, t):
        '''Changes "t" ie thickness paramater for each bolt in each row
        '''
        for row in self.rows:
            for bolt in row.bolts:
                bolt.t = t
    
    def changeTp(self, tp):
        '''Changes "tp" ie thickness of plate for each bolt in each row
        '''
        t = self.member.t
        teff = (t - tp) / 2
        for row in self.rows:
            for bolt in row.bolts:
                bolt.tp = tp
                bolt.t = teff
    
    def changeRo(self, ro):
        '''Changes "ro" for each bolt in group
        '''
        for row in self.rows:
            for bolt in row.bolts:
                bolt.ro = ro
    def changeRoM(self, roM):
        '''Changes "roM" for each bolt in group
        '''
        for row in self.rows:
            for bolt in row.bolts:
                bolt.roM = roM
    
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
    
    def boltVectors(self):
        '''to each bolt in self.rows adds:
        
        vector [from bolt coortinates to ctr of stifness]
        lengt [length of vector]
        }
        '''
        ctr = self.ctrStifness()
        for row in self.rows:
            for bolt in row.bolts:
                coor = bolt.coordinates
                vector = [coor[0] - ctr[0] + 0.0001, coor[1] - ctr[1] + 0.0001] #0.0001 added so that the x or y is never zero
                length = (vector[0] **2 + vector[1] ** 2) ** 0.5
                if hasattr(bolt, "vector"):
                    bolt.vector = vector
                    bolt.length = length
                else:
                    setattr(bolt,"vector",vector)
                    setattr(bolt,"length",length)
        return ctr
    
    def forceFromMoment(self, moment):
        '''to each bolt in self.rows adds:        
        
        resMoment = {
            force: float in N
            vector: [] vector of force direction... length corresponds to force
        }
        moment = [kNm]
        '''
        ctr = self.boltVectors() #updates boltVectors
        M = moment * 10**6 #moment in Nmm
        if M >= 0:
            xDir = [1,-1] #x direction of vector above / bellow of ctr of stifness
        else:
            xDir = [1,-1]
        self.boltVectors()
        sumBolts = 0
        for row in self.rows:
            for bolt in row.bolts:
                sumBolts += bolt.length ** 2 * bolt.kSer()
        
        for row in self.rows:
            for bolt in row.bolts:
                resMoment = {"force": 0, "vector": []}
                force = M * bolt.length * bolt.kSer()/ sumBolts
                resMoment["force"] = force                
                x1 = bolt.vector[0]
                y1 = bolt.vector[1]
                if bolt.coordinates[1] >= ctr[1]: #if bolt is above ctr of stifness:
                    x2 = xDir[0]
                else:
                    x2 = xDir[1]
                y2 = x1 * x2 / y1 * -1
                length = (x2 ** 2 + y2 ** 2) ** 0.5
                vector = [x2 / length * force, y2 / length * force]
                resMoment["vector"] = vector
                if hasattr(bolt, "resMoment"):
                    bolt.resMoment = resMoment
                else:
                    setattr(bolt,"resMoment", resMoment)
    
    def forceFromForces(self,V,N):
        '''to each bolt in self.rows adds:
        
        resForces:{
            force: float in N
            vector: [] vector of force direction... length corresponds to force
        }
        V = shear force in kN (+ is from up to down)
        N = axial force in kN (+ is from left to right)
        '''        
        n = 0
        for row in self.rows:
            n += row.n()
        
        V = V * 1000 / n
        N = N * 1000 / n
        
        force = (V ** 2 + N ** 2) ** 0.5
        vector = [-N, V]
        resForces = {
            'force': force,
            'vector': vector        
        }
        for row in self.rows:
            for bolt in row.bolts:
                if hasattr(bolt,'resForces'):
                    bolt.resForces = resForces
                else:
                    setattr(bolt, 'resForces', resForces)
    
    def forceOnBolts(self,M,V,N):
        '''to each bolt in self.rows adds:
        
        resForce: float in N
        ...and updates parameter alpha in degrees
        M... moment in kNm
        V... shear in kN
        N... axial in iN
        '''
        self.forceFromMoment(M)
        self.forceFromForces(V,N)
        unit = [-1,0] #unit vector to which alfa is being calculated
        unitLength = (unit[0] ** 2 + unit[1] ** 2) ** 0.5
        for row in self.rows:
            for bolt in row.bolts:
                fm = bolt.resMoment["vector"]
                fn = bolt.resForces["vector"]
                x = fm[0] + fn [0]
                y = fm[1] + fn [1]
                resForce = (x ** 2 + y ** 2) ** 0.5
                resVector = [x,y]
                dotProduct = resVector[0] * unit[0] + resVector[1] * unit[1]
                mod = resForce * unitLength + 0.0001
                cosAlpha = dotProduct / mod
                alpha = math.degrees(math.acos(cosAlpha))
                if y >= 0:
                    alpha = 360 - alpha #basic alpha is only between 0 - 180 degree... if vector y axis is + then adjust for this
                bolt.alfa = alpha
                if hasattr(bolt,'resForce'):
                    bolt.resForce = resForce
                else:
                    setattr(bolt, 'resForce', resForce)
                
                
                
    

                
            
                          

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



