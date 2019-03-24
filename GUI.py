#--------------------------------------------------------------------------------
# GUI for handling the tsunami simulation scenario file in ANUGA
# by febrifahmi<fahmi_fafa@yahoo.com>
#--------------------------------------------------------------------------------
import Tkinter
box = Tkinter.Tk()
# start coding here..

class Application(Tkinter.Frame):
	bg = Tkinter.Canvas(box, width=450, height=350)
	windowx = bg.create_window(0, 0, width=400, height=300)
	def createWidgets(self):
			self.quitButton = Tkinter.Button(self, text='Quit',
				command=self.quit)
			self.quitButton.grid()

	def __init__(self, master=bg):
		Tkinter.Frame.__init__(self, master)
		self.grid_bbox(0,0,6,6)
		self.grid()
		self.createWidgets()

box = Application()
box.master.title('ANUGA Scenario maker v 1.0')
box.mainloop()