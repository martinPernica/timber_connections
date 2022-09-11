import typer
import tkinter
import math
import connectors
import groupOfBolts


class drawConnection():

    def __init__(self,main, member, group, margins = [40,40,40,40]):
        '''main: main window of tkinter
        '''
        self.main = main
        self.pict = tkinter.Canvas(self.main, height = 250, width = 300, bg = "green")
        self.pict.pack()
        self.pict.update() #update to get correct widget sizes
        self.member = member #instance of groupOfBolts.Member
        self.group = group #instance of groupOfBolts.GroupOfBolts
        self.margins = margins #margins in pixels
        print(self.pict.winfo_width())
        print(self.pict.winfo_height())
    
    def maxX(self):
        '''calculates maximal X coordinate of any bolt relative to member reference point
        '''
        for row in group.rows:
            maxX = 0
            for bolt in row.bolts:
                x = bolt.coordinates[0]
                if x > maxX:
                    maxX = x
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
            print("printing line from {} to {}".format(dPts[i], dPts[i+1]))
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
            startX = row.start[0] #coortinates relative to center of member
            startY = row.start[1] #in groupFoBolts model Y is up, in canvas Y is down            

            for bolt in row.bolts:    
                x = ctr[0] + bolt.coordinates[0] * scale
                y = ctr[1] - bolt.coordinates[1] * scale
                self.drawBolt([x,y])
    
    def drawConnection(self):
        drawParams = self.drawTimber() #draws timber + extracts drawing parameters
        scale = drawParams["scale"]
        ctr = drawParams["ctr"]
        self.drawGroupOfBolts(ctr, scale)
        self.main.mainloop()

class ConnInput():

    def __init__(self):
        '''this class is a container for input methods
        '''
    
    def createMember(delf):
        print("member width in [mm] = ")
        b = float(input())
        print("member height in [mm] =")
        h = float(input())




bolts1 = []
for i in range(0,5):
    bolt = connectors.bolt(16,460,350,50*i,100)
    bolts1.append(bolt)
    
bolts2 = []
for i in range(0,5):
    bolt = connectors.bolt(16,460,350,50*i,100)
    bolts2.append(bolt)
    
bolts3 = []
for i in range(0,5):
    bolt = connectors.bolt(16,460,350,50*i,100)
    bolts3.append(bolt)
    


row1 = groupOfBolts.Row([80 + 100 * math.tan(45/180*math.pi),100],16*9,bolts1)
row2 = groupOfBolts.Row([80 - 100 * math.tan(45/180*math.pi),-100],16*9,bolts2)
row3 = groupOfBolts.Row([80,0],16*9,bolts3) 

member = groupOfBolts.Member(120, 360, 45)
group = groupOfBolts.GroupOfBolts([row1, row2, row3], member)

main = tkinter.Tk()
connection = drawConnection(main, member, group)
connection.drawConnection()


#pict.pack()
#top.mainloop()