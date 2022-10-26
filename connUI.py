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
window.columnconfigure(1,weight = 1, minsize = 200)
window.rowconfigure(1, weight = 1, minsize = 100)
canvasContainer.grid(row = 1, column = 1, padx = 10, pady = 10)

#container for timber input
timberContainer = tk.Frame(
    master = window,
    relief = tk.GROOVE,
    borderwidth = 10,
)
timberContainer.grid(row = 2, column = 1, padx = 10, pady = 10)
window.rowconfigure(2, weight = 1, minsize = 50)

window.mainloop()
