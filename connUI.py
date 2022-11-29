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
timbLabels = ["h = ", "b = ", "\u03b1 =", "\u03c1k =", "\u03c1m =", "tp ="]
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
ent_timbRoM = tk.Entry(master = timberContainer)
ent_timbRoM.grid(row = 4, column = 1)
ent_plateThick = tk.Entry(master = timberContainer)
ent_plateThick.grid(row = 5, column = 1)

#...timber input units
i = 0
timbUnits = ["mm", "mm", "\u00b0", "kg/m3", "kg/m3", "mm"]
for unit in timbUnits:
    label = tk.Label(master = timberContainer, text = unit)
    label.grid(row = i, column = 2)
    i += 1
    
#...timber change input button
btn_timb = tk.Button(
    master = timberContainer, 
    text = "nastavit",
    command = lambda: changeMember(ent_timbHeight, ent_timbBreadth, ent_timbBeta, ent_timbRo, ent_timbRoM, ent_plateThick, member, connection, textOutputConnection, group)
)
btn_timb.grid(row = 6, column = 1)

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

#intput text info
inputTextContainer = tk.Frame(
    master = window,
    relief = tk.GROOVE,
    borderwidth = 5,
)

inputTextContainer.grid(column = 0, row = 2, sticky = "nsew", columnspan = 2)
text_member = tk.Text(master = inputTextContainer, height = 10)
text_member.pack()

#acting forces input
inputForcesContainer = tk.Frame(
    master = window,
    relief = tk.GROOVE,
    borderwidth = 5
)

inputForcesContainer.grid(column = 0, row = 3, sticky = "nsew", columnspan = 2)
for i in range(0,6):
    inputForcesContainer.columnconfigure(i,minsize = 150)
#...acting forces input fields
force_labs = ["Moment", "Posouvací síla", "Normálová síla"]
force_units = ["kNm", "kN", "kN"]

i = 0
for lab in force_labs:
    lab_desc = tk.Label(master = inputForcesContainer, text = lab)
    lab_desc.grid(row = 1, column = i * 2, columnspan = 2, sticky = "ew")
    i += 1

inp_mom = tk.Entry(master = inputForcesContainer)
inp_mom.grid(row = 2, column = 0)
inp_shear = tk.Entry(master = inputForcesContainer)
inp_shear.grid(row = 2, column = 2)
inp_axial = tk.Entry(master = inputForcesContainer)
inp_axial.grid(row = 2, column = 4)

i = 0
for unit in force_units:
    lab_unit = tk.Label(master = inputForcesContainer, text = unit)
    lab_unit.grid(row = 2, column = i * 2 + 1)
    i += 1

#...calculate button
btn_calc = tk.Button(
    master = inputForcesContainer,
    text = "Spočítat",
    command = lambda: calculateResults(group),
)
btn_calc.grid(row = 3, column = 0)

#output text info
outputTextContainer = tk.Frame(
    master = window,
    relief = tk.GROOVE,
    borderwidth = 5,
)

outputTextContainer.grid(column = 0, row = 4, sticky = "nsew", columnspan = 2)
text_output = tk.Text(master = outputTextContainer, height = 10)
text_output.pack()

for i in range(2):
    print(i)
    window.columnconfigure(i,weight=1,minsize = 75)

for i in range(5):
    window.rowconfigure(i,weight = 1, minsize = 75)

#handler functions
def changeMember(h_input, b_input, beta_input,ro_input,roM_input, tp_input, member,connection, textOutputConnection, groupOfBolts):
    try:
        h = int(h_input.get())
        member.changeH(h)
    except:
        pass
    try:
        b = int(b_input.get())
        member.changeT(b)
        t = (member.t - member.tp) / 2
        groupOfBolts.changeT(t)
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
        groupOfBolts.changeRo(ro)
    except:
        pass
    try:
        roM = int(roM_input.get())
        member.changeRoM(roM)
        groupOfBolts.changeRoM(roM)
    except:
        pass
    try:
        tp = int(tp_input.get())
        member.changeTp(tp)
        groupOfBolts.changeTp(tp)
    except:
        pass
    connection.drawConnection()
    textOutputConnection.textOutput()
    text_output.delete("1.0", tk.END)

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
    roM = member.roM
    t = (member.t - member.tp) / 2
    bolts = []
    for i in range(n):
        bolt = connectors.bolt(d, fu, ro, 0, t, roM = roM)
        bolts.append(bolt)
    row = groupOfBolts.Row([x,y], a1, bolts)
    group.addRow(row)
    connection.drawConnection()
    textOutputConnection.textOutput()
    text_output.delete("1.0", tk.END)

def remBolts(rowNumber_input, group, connection):
    try:
        no = int(rowNumber_input.get())
    except:
        return
    group.deleteRow(no)
    connection.drawConnection()
    textOutputConnection.textOutput()
    text_output.delete("1.0", tk.END)
    
#calclulate results

def calculateResults(group):
    ctr = group.ctrStifness()
    try:
        moment = float(inp_mom.get())
    except:
        moment = 0
    try:
        shear = float(inp_shear.get())
    except:
        shear = 0
    try:
        axial = float(inp_axial.get())
    except:
        axial = 0
    group.forceOnBolts(moment, shear, axial)
    group.designShearResistance()
    textOutputResults.textOutput()
    

if __name__ == "__main__":
    bolts1 = []
    for i in range(0,2):
        bolt = connectors.bolt(16,460,350,0*i,200, roM = 450)
        bolts1.append(bolt)
        
    bolts2 = []
    for i in range(0,2):
        bolt = connectors.bolt(16,460,350,50*i,200, roM = 450)
        bolts2.append(bolt)
        
    member = groupOfBolts.Member(120, 360, 0)
    group = groupOfBolts.GroupOfBolts([], member)

    connection = drawingScripts.drawConnection(canvasContainer, member, group)
    connection.drawConnection()
    
    textOutputConnection = drawingScripts.textOutputConnection(text_member, member, group)
    textOutputConnection.textOutput()
    
    textOutputResults = drawingScripts.textOutputResults(text_output, group)

window.mainloop()
