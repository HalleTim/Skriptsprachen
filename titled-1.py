import microInput
from matplotlib.figure import Figure
import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
recorder = microInput.Recorder()

input= recorder.recordAudio()


root = tkinter.Tk()
root.wm_title("Embedding in Tk")

fig= Figure(figsize=(5, 4), dpi=100)

fig.add_subplot(111).plot(input)
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)



tkinter.mainloop()