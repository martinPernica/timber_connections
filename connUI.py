import tkinter
import math
import connectors
import groupOfBolts


class drawConnection():

    def __init__(self,member, group, margins = [40,40,40,40]):
        self.main = tkinter.Tk()
        self.pict = tkinter.Canvas(self.main, height = 250, width = 300, bg = "green")
        self.pict.pack()
        self.pict.update() #update to get correct widget sizes
        self.member = member #instance of groupOfBolts.Member
        self.group = group #instance of groupOfBolts.GroupOfBolts
        self.margins = margins #margins in pixels
        print(self.pict.winfo_width())
        print(self.pict.winfo_height())
    
    def drawTimber(self):
        '''method that draws the timber
        
        return value = scale of drawing to canvas
        '''
        h = self.member.h #mm
        beta = self.member.beta / 180 * math.pi # degree
        maxX = 600 #mm max X coordinate of any bolt in connection
        
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
        
        for i in range(0,len(dPts)-1):
            print("printing line from {} to {}".format(dPts[i], dPts[i+1]))
            self.pict.create_line(dPts[i][0],dPts[i][1],dPts[i+1][0],dPts[i+1][1])
        
        return scale
    
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

    
    
    def drawConnection(self):
        scale = self.drawTimber()
        self.drawBolt([150,150])
        self.main.mainloop()

bolts = []
for i in range(0,3):
    bolt = connectors.bolt(16,460,350,50*i,100)
    bolts.append(bolt)

row1 = groupOfBolts.Row([80,140],16*15,bolts)
row2 = groupOfBolts.Row([80,-140],16*7,bolts)
row3 = groupOfBolts.Row([80,0],16*7,bolts) 

member = groupOfBolts.Member(120, 360, 35)
group = groupOfBolts.GroupOfBolts([row1, row2, row3], member)
 
connection = drawConnection(member)
connection.drawConnection()


#pict.pack()
#top.mainloop()