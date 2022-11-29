import typer
import tkinter
import math
import connectors
import groupOfBolts


class drawConnection():

    def __init__(self,container, member, group, margins = [40,40,40,40]):
        '''main: main window of tkinter
        '''
        self.container = container
        self.pict = tkinter.Canvas(self.container, bg = "green")
        self.pict.grid(row=0, column=0, sticky = "nsew")
        self.pict.update() #update to get correct widget sizes
        self.member = member #instance of groupOfBolts.Member
        self.group = group #instance of groupOfBolts.GroupOfBolts
        self.margins = margins #margins in pixels
        #print(self.pict.winfo_width())
        #print(self.pict.winfo_height())
    
    def maxX(self):
        '''calculates maximal X coordinate of any bolt relative to member reference point
        '''
        maxX = 0
        try: #try for the case there is any member
            for row in self.group.rows:
                maxX = 0
                for bolt in row.bolts:
                    x = bolt.coordinates[0]
                    if x > maxX:
                        maxX = x
        except:
            pass
        return maxX
    
    def drawTimber(self):
        '''method that draws the timber
        
        return value = scale of drawing to canvas
        '''
        h = self.member.h #mm
        beta = self.member.beta / 180 * math.pi # degree
        maxX = self.maxX() + (h/2) * math.tan(beta) #mm max X coordinate of any bolt in connection relative to tip P2 or P3 whichever gives greater value
        
        #define abs coordinates
        p1 = [maxX + 200, 0]
        p2 = [h * math.tan(beta), 0]
        p3 = [0, h]
        p4 = [maxX + 200, h]    
               
        #define scale       
        xLen = max(p1[0] - p2[0], p4[0] - p3[0])
        yLen = abs(p2[1] - p3[1])
        canvasWidth = self.pict.winfo_width()
        canvasHeight = self.pict.winfo_height()
        availableWidth = canvasWidth - self.margins[1] - self.margins[3]
        availableHeight = canvasHeight - self.margins[0] - self.margins[2]
        scaleX = availableWidth / xLen
        scaleY = availableHeight / yLen
        scale = min(scaleX, scaleY)
        
        #create coordinates
        dPts = []
              
        for point in [p1, p2, p3, p4]:
            pt = [item * scale for item in point]
            dPts.append(pt)
        
        for i in range(0, len(dPts)):
            dPts[i][0] = dPts[i][0] + self.margins[1]
            dPts[i][1] = dPts[i][1] + self.margins[0] 
            
        #draw timber
        for i in range(0,len(dPts)-1):
            #print("printing line from {} to {}".format(dPts[i], dPts[i+1]))
            self.pict.create_line(dPts[i][0],dPts[i][1],dPts[i+1][0],dPts[i+1][1])
        
        #calculate coordinates of the CTR point on canvas. i.e. intersection of timber center line with end line of timber
        ctr = [(dPts[1][0]+dPts[2][0])/2,(dPts[1][1]+dPts[2][1])/2] #[x, y] in pixels
        
        return {
            "scale": scale,
            "ctr": ctr,
            }
    
    def drawBolt(self, ctr, size = 20):
        '''draws signe i.e. cross representing bolt
        
        ctr = [x,y] # in pixels  
        size #in pixels, size of cross
        '''
        x = ctr[0]
        y = ctr[1]
        arm = size / 2
        p1 = [x - arm, y]
        p2 = [x + arm, y]
        p3 = [x, y - arm]
        p4 = [x, y + arm]
        
        self.pict.create_line(p1[0],p1[1],p2[0],p2[1])
        self.pict.create_line(p3[0],p3[1],p4[0],p4[1])
    
    def drawGroupOfBolts(self, ctr, scale):
        '''Draws all bolts from "group" parameter
        '''
        for row in self.group.rows:
            startX = row.start[0] #coordinates relative to center of member
            startY = row.start[1] #in groupFoBolts model Y is up, in canvas Y is down            

            for bolt in row.bolts:    
                x = ctr[0] + bolt.coordinates[0] * scale
                y = ctr[1] - bolt.coordinates[1] * scale
                self.drawBolt([x,y])
                
    def drawRowAxes(self, ctr, scale):
        for row in self.group.rows:
            startX = ctr[0] + row.bolts[0].coordinates[0] * scale
            startY = ctr[1] - row.bolts[0].coordinates[1] * scale
            endX = ctr[0] + row.bolts[-1].coordinates[0] * scale
            endY = ctr[1] - row.bolts[-1].coordinates[1] * scale
            print("startY = {}, endY = {}".format(startY, endY))
            
            self.pict.create_line(startX,startY,endX,endY, fill = "red")
            
    def drawLineNumbers(self,ctr, scale):
        for row in self.group.rows:
            no = row.no
            x = ctr[0] + row.start[0] * scale - 20
            y = ctr[1] - row.start[1] * scale
            self.pict.create_text(x, y, text = no, fill = "orange")
    
    def drawConnection(self):
        self.pict.delete("all") #clear canvas
        drawParams = self.drawTimber() #draws timber + extracts drawing parameters
        scale = drawParams["scale"]
        ctr = drawParams["ctr"]
        self.drawRowAxes(ctr, scale)
        self.drawGroupOfBolts(ctr, scale) 
        self.drawLineNumbers(ctr, scale)
        #self.container.mainloop()

class textOutputConnection():
    '''member = instance of member class
    groupOfBolts = instance of groupOfBolts class
    textWidget = instance of tk.Text widget
    '''
    def __init__(self, textWidget, member, groupOfBolts = 1):
        self.member = member
        self.groupOfBolts = groupOfBolts
        self.textWidget = textWidget
    
    def fillGaps(self,tab, lineNo):
        index = str(lineNo)+ "." + str(0)
        length = len(self.textWidget.get(index,"end"))
        while True:
            if tab > length:
                self.textWidget.insert("end"," ")
                length = len(self.textWidget.get(index,"end"))
            else:
                break
    
    def nextLine(self):
        return int(self.textWidget.index('end').split(".")[0])
    
    def memberString(self):
        '''writes string describing member
        '''
        tabs = [0, 10, 20, 30, 45, 60]
        header = ["h [mm]", "b [mm]", "\u03b1 [\u00b0]", "\u03c1k [kg/m3]", "\u03c1k [kg/m3]", "tp [mm]"]
        i = 0
        for col in tabs:
            pos = str(1) + "." + str(col)
            self.fillGaps(col,1)
            self.textWidget.insert(pos,header[i])
            i += 1
        self.textWidget.insert("end","\n")
        vals = []
        vals.append(self.member.h)
        vals.append(self.member.t)
        vals.append(self.member.beta)
        vals.append(self.member.ro)
        vals.append(self.member.roM)
        vals.append(self.member.tp)
        i = 0
        for col in tabs:
            pos = str(2) + "." + str(col)
            self.fillGaps(col,2)
            self.textWidget.insert(pos,vals[i])
            i += 1    
    
    def boltsString(self):
        '''writes string describing groupOfBolts
        '''
        pos = str(self.nextLine()) + "." + str(0)
        self.textWidget.insert(pos, "SKUPINA ŠROUBŮ\n")
        tabs = [0, 10, 20, 30,40,50,60]
        header = ["no", "d [mm]", "fu [MPa]", "X [mm]", "Y [mm]", "n [-]", "a1 [mm]"]
        i = 0
        for col in tabs:
            pos = str(self.nextLine()) + "." + str(0)
            self.fillGaps(col,self.nextLine()-1)
            self.textWidget.insert(pos,header[i])
            i += 1
        self.textWidget.insert("end", "\n")
        for row in self.groupOfBolts.rows:
            vals = []
            vals.append(int(row.no))
            vals.append(int(row.bolts[0].d))
            vals.append(int(row.bolts[0].fu))
            vals.append(int(row.start[0]))
            vals.append(int(row.start[1]))
            vals.append(int(row.n()))
            vals.append(int(row.a1))
            i = 0
            for col in tabs:
                pos = str(self.nextLine()) + "." + str(col)
                self.fillGaps(col, self.nextLine()-1)
                self.textWidget.insert(pos,vals[i])
                i += 1
            self.textWidget.insert("end", "\n")
        
    
    def textOutput(self):
        self.textWidget.delete("1.0", tkinter.END)
        self.memberString()
        self.textWidget.insert("end","\n\n")
        self.boltsString()
    
class textOutputResults():
    '''class handling texto output of results
    '''
    def __init__(self, textWidget, groupOfBolts):
        '''text widget = instance of tk.Text
        groupOfBolts = instance of scripts.groupOfBolts
        '''
        self.textWidget = textWidget
        self.groupOfBolts = groupOfBolts
        
    def fillGaps(self,tab, lineNo):
        index = str(lineNo)+ "." + str(0)
        length = len(self.textWidget.get(index,"end"))
        while True:
            if tab > length:
                self.textWidget.insert("end"," ")
                length = len(self.textWidget.get(index,"end"))
            else:
                break
    
    def nextLine(self):
        return int(self.textWidget.index('end').split(".")[0])
        
    def ctrStifnessOutput(self):
        '''function printing out coordinates of ctr of stifness
        '''
        self.textWidget.insert("1.0", "POZICE STŘEDU OTÁČENÍ\n")
        ctr = self.groupOfBolts.ctrStifness()
        X = round(ctr[0]*10)/10
        Y = round(ctr[1]*10)/10
        string = "X = {} mm, Y = {} mm".format(X,Y)
        pos = str(self.nextLine()) + "." + "0"
        self.textWidget.insert(pos, string)
    
    def designOutput(self):
        '''function pringint out acting forces
        '''
        pos = str(self.nextLine()) + "." + "0"
        print("POZICE: {}".format(pos))
        self.textWidget.insert(pos, "\n\nSÍLY PŮSOBÍCÍ NA ŠROUBY\n")
        tabs = [0, 10, 20, 30, 40, 50, 60]
        header = ["šroub", "Fed [N]", "alfa [stup]", "Fvrk0 [N]", "Fvrk90 [N]", "nef [-]", "Fvrk [N]"]
        i = 0
        for col in tabs:
            pos = str(self.nextLine()) + "." + str(0)
            self.fillGaps(col,self.nextLine()-1)
            self.textWidget.insert(pos,header[i])
            i += 1
        self.textWidget.insert("end", "\n")
        for row in self.groupOfBolts.rows:
            n = 1
            rowNo = row.no
            neff = round(row.neff()*100)/100
            for bolt in row.bolts:                
                boltNo = str(rowNo) + "-" + str(n)
                force = int(bolt.resForce)
                alfa = int(bolt.alfa)
                Fvrk0 = int(bolt.Fvrk0)
                Fvrk90 = int(bolt.Fvrk90)      
                Fvrk = int(bolt.Fvrk)
                vals = [boltNo, force, alfa, Fvrk0, Fvrk90, neff, Fvrk]
                nextLine = self.nextLine()
                n += 1
                j = 0
                for col in tabs:
                    self.fillGaps(col, nextLine - 1)
                    pos = str(nextLine) + "." + str(col)
                    self.textWidget.insert(pos, str(vals[j]))
                    j += 1
                self.textWidget.insert("end", "\n")
        
        
    def textOutput(self):
        '''wrapper function to create text output of results
        '''
        self.textWidget.delete("1.0", tkinter.END)
        self.ctrStifnessOutput()
        self.designOutput()

        
        

if __name__ == "__main__":
    bolts1 = []
    for i in range(0,5):
        bolt = connectors.bolt(16,460,350,0*i,100)
        bolts1.append(bolt)
        
    bolts2 = []
    for i in range(0,5):
        bolt = connectors.bolt(16,460,350,50*i,100)
        bolts2.append(bolt)
        


    row1 = groupOfBolts.Row([80 + 100 * math.tan(45/180*math.pi),100],16*9,bolts1)
    row2 = groupOfBolts.Row([80 - 100 * math.tan(45/180*math.pi),-100],250,bolts2)


    member = groupOfBolts.Member(120, 360, 0)
    group = groupOfBolts.GroupOfBolts([row1, row2, row3], member)
    group.designShearResistance(toPrint = True)

    main = tkinter.Tk()
    connection = drawConnection(main, member, group)
    connection.drawConnection()
    
    print("window was closed")


    #pict.pack()
    #top.mainloop()