import typer
import tkinter as tk
import math
from scripts import connectors
from scripts import groupOfBolts
from scripts import drawingScripts

window = tk.Tk()

#container for canvas
canvasContainer = tk.Frame(
    master = window,
    relief = tk.GROOVE,
    borderwidth = 5
)
canvasContainer.grid(row = 0, column = 0, padx = 0, pady = 0, sticky = "nsew", rowspan = 2)
#label1 = tk.Label(master = canvasContainer, text = "here Will Be Canvas")
#label1.pack(padx = 10, pady = 10)

#container for timber input
timberContainer = tk.Frame(
    master = window,
    relief = tk.GROOVE,
    borderwidth = 5,
)
timberContainer.grid(row = 0, column = 1, padx = 0, pady = 0, sticky = "nsew")
label2 = tk.Label(master = timberContainer, text = "here will be timber input")
label2.pack(padx = 10, pady = 10)

boltContainer = tk.Frame(
    master = window,
    relief = tk. GROOVE,
    borderwidth = 5
)

boltContainer.grid(row=1,column=1, sticky = "nsew")
label3 = tk.Label(master = boltContainer, text = "bolt container")
label3.pack(padx = 10, pady = 10)

for i in range(2):
    print(i)
    window.columnconfigure(i,weight=1,minsize = 75)

for i in range(2):
    window.rowconfigure(i,weight = 1, minsize = 75)

if __name__ == "__main__":
    bolts1 = []
    for i in range(0,5):
        bolt = connectors.bolt(16,460,350,0*i,100)
        bolts1.append(bolt)
        
    bolts2 = []
    for i in range(0,1):
        bolt = connectors.bolt(16,460,350,0*i,100)
        bolts2.append(bolt)
        
    bolts3 = []
    for i in range(0,5):
        bolt = connectors.bolt(16,460,350,50*i,100)
        bolts3.append(bolt)
        


    row1 = groupOfBolts.Row([80 + 100 * math.tan(45/180*math.pi),100],16*9,bolts1)
    row2 = groupOfBolts.Row([80 - 100 * math.tan(45/180*math.pi),-100],250,bolts2)
    row3 = groupOfBolts.Row([80,0],16*9,bolts3) 

    member = groupOfBolts.Member(120, 360, 45)
    group = groupOfBolts.GroupOfBolts([row1, row2, row3], member)
    group.designShearResistance(toPrint = True)

    connection = drawingScripts.drawConnection(canvasContainer, member, group)
    connection.drawConnection()

window.mainloop()
