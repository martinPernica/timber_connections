import tkinter
import math


class drawConnection():

    def __init__(self):
        self.main = tkinter.Tk()
        self.pict = tkinter.Canvas(self.main, height = 250, width = 300)
        self.pict.pack()
        self.pict.update() #update to get correct widget sizes
        print(self.pict.winfo_width())
        print(self.pict.winfo_height())
    
    def drawTimber(self):
        '''method that draws the timber
        
        return value = scale of drawing to canvas
        '''
        h = 360 #mm
        beta = 25 / 180 * math.pi # degree
        maxX = 200 #mm max X coordinate of any bolt in connection
        margins = [40,40,40,40] #margins in pixels
        
        #define abs coordinates
        p1 = [maxX + 200, h / 2]
        p2 = [(h / 2) * math.tan(beta), h / 2]
        p3 = [-(h / 2) * math.tan(beta), -h / 2]
        p4 = [maxX + 200, -h / 2]    
               
        #define scale
        xLen = p2[1] - p3[1]
        yLen = max(p1[0] - p2[0], p4[0] - p3[0])
        canvasWidth = self.pict.winfo_width()
        canvasHeight = self.pict.winfo_height()
        availableWidth = canvasWidth - margins[1] - margins[3]
        availableHeight = canvasHeight - margins[0] - margins[2]
        scaleX = availableWidth / xLen
        scaleY = availableHeight / yLen
        scale = min(scaleX, scaleY)
        
        #drawTimberOutline
        dPts = []
        for point in [p1, p2, p3, p4]:
            pt = [item * scale for item in point]
            dPts.append(pt)   
            print(pt)
        
        for i in range(0,len(dPts)-1):
            print("printing line from {} to {}".format(dPts[i], dPts[i+1]))
            self.pict.create_line(dPts[i][0],dPts[i][1],dPts[i+1][0],dPts[i+1][1])
        
        self.main.mainloop()
        
        
        
        
        
        
        



connection = drawConnection()
connection.drawTimber()


#pict.pack()
#top.mainloop()