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
#...timber input labels
timbLabels = ["h = ", "b = ", "\u03b1 =", "\u03c1 ="]
i = 0
for lab in timbLabels:
    label = tk.Label(master = timberContainer, text = lab)
    label.grid(row = i, column = 0)
    i += 1

#...timber input entries
#timbEntr = ["ent_timbHeight", "ent_timbBreadth", "ent_timbBeta"]

ent_timbHeight = tk.Entry(master = timberContainer)
ent_timbHeight.grid(row = 0, column = 1)
ent_timbBreadth = tk.Entry(master = timberContainer)
ent_timbBreadth.grid(row = 1, column = 1)
ent_timbBeta = tk.Entry(master = timberContainer)
ent_timbBeta.grid(row = 2, column = 1)
ent_timbRo = tk.Entry(master = timberContainer)
ent_timbRo.grid(row = 3, column = 1)

#...timber input units
i = 0
timbUnits = ["mm", "mm", "\u00b0", "kg/m3"]
for unit in timbUnits:
    label = tk.Label(master = timberContainer, text = unit)
    label.grid(row = i, column = 2)
    i += 1
    
#...timber change input button
btn_timb = tk.Button(
    master = timberContainer, 
    text = "nastavit",
    command = lambda: changeMember(ent_timbHeight, ent_timbBreadth, ent_timbBeta, ent_timbRo, member, connection)
)
btn_timb.grid(row = 4, column = 1)

#bolt group input
boltContainer = tk.Frame(
    master = window,
    relief = tk. GROOVE,
    borderwidth = 5
)

boltContainer.grid(row=1,column=1, sticky = "nsew")
#...bolt input labels
boltLabels = ["d =", "fu =", "x =", "y =", "n =", "a1 ="]
i = 0
for lab in boltLabels:
    label = tk.Label(master = boltContainer, text = lab)
    label.grid(row = i, column = 0)
    i += 1

#...bolt input entries
ent_boltDia = tk.Entry(master = boltContainer)
ent_boltDia.grid(column = 1, row = 0)
ent_boltFu = tk.Entry(master = boltContainer)
ent_boltFu.grid(column = 1, row = 1)
ent_boltX = tk.Entry(master = boltContainer)
ent_boltX.grid(column = 1, row = 2)
ent_boltY = tk.Entry(master = boltContainer)
ent_boltY.grid(column = 1, row = 3)
ent_boltN = tk.Entry(master = boltContainer)
ent_boltN.grid(column = 1, row = 4)
ent_boltA1 = tk.Entry(master = boltContainer)
ent_boltA1.grid(column = 1, row = 5)

#...bolt input units
boltUnits = ["mm", "MPa", "mm", "mm","-", "mm"]
i = 0
for lab in boltUnits:
    label = tk.Label(master = boltContainer, text = lab)
    label.grid(row = i, column = 2)
    i += 1

#...bolt row input button
btn_boltAdd = tk.Button(
    master = boltContainer,
    text = "vložit řadu",
    command = lambda:addBolts(ent_boltDia, ent_boltFu, ent_boltX, ent_boltY, ent_boltN, ent_boltA1, member, group, connection)
    )
btn_boltAdd.grid(column = 1, row = 6)

#bolt row number input
lab_rowNo = tk.Label(master = boltContainer, text = "číslo řady:")
lab_rowNo.grid(column = 0, row = 7 )
ent_rowNo = tk.Entry(master = boltContainer)
ent_rowNo.grid(column = 1, row = 7)
btn_boltRemove = tk.Button(
    master = boltContainer,
    text = "smazat řadu",
    command = lambda: remBolts(ent_rowNo, group, connection)
    )
btn_boltRemove.grid(column = 0, row = 8)

#acting forces input
inputTextContainer = tk.Frame(
    master = window,
    relief = tk. GROOVE,
    borderwidth = 5
)

inputTextContainer.grid(column = 0, row = 2, sticky = "nsew", columnspan = 2)
text_member = tk.Text(master = inputTextContainer)
text_member.pack()



for i in range(2):
    print(i)
    window.columnconfigure(i,weight=1,minsize = 75)

for i in range(3):
    window.rowconfigure(i,weight = 1, minsize = 75)

#handler functions
def changeMember(h_input, b_input, beta_input,ro_input, member,connection):
    try:
        h = int(h_input.get())
        member.changeH(h)
    except:
        pass
    try:
        b = int(b_input.get())
        member.changeT(b)
    except:
        pass
    try:        
        beta = int(beta_input.get())
        member.changeBeta(beta)
    except:
        pass
    try:
        ro = int(ro_input.get())
        member.changeRo(ro)
    except:
        pass
    connection.drawConnection()
    textOutputConnection.textOutput()

def addBolts(d_input, fu_input, x_input, y_input, n_input, a1_input, member, group, connection):
    try:
        d = int(d_input.get())
        fu = int(fu_input.get())
        x = int(x_input.get())
        y = int(y_input.get())
        n = int(n_input.get())
        a1 = int(a1_input.get())
    except:
        return
    ro = member.ro
    t = member.t/2
    bolts = []
    for i in range(n):
        bolt = connectors.bolt(d, fu, ro, 0, t)
        bolts.append(bolt)
    row = groupOfBolts.Row([x,y], a1, bolts)
    group.addRow(row)
    connection.drawConnection()
    textOutputConnection.textOutput()

def remBolts(rowNumber_input, group, connection):
    try:
        no = int(rowNumber_input.get())
    except:
        return
    group.deleteRow(no)
    connection.drawConnection()
    textOutputConnection.textOutput()

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
    
    textOutputConnection = drawingScripts.textOutputConnection(text_member, member, group)
    textOutputConnection.textOutput()

window.mainloop()
