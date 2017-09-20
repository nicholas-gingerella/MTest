import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pyautogui
import csv

duration = 0.1
screenSizeX, screenSizeY = pyautogui.size()

class Application(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master.title("MTest")
		self.master.resizable(False, False)
		self.master.attributes("-topmost", True)
		self.master.configure(background="#eaf2ff")
		# self.grid()
		self.pack()
		self.create_widgets()
		self.point_list = []
		self.currentTestPointFile = tk.StringVar()

		
	def create_widgets(self):
		self.widgetWidths = 25
		self.openPointsBtn = tk.Button(self)
		self.openPointsBtn["text"] = "Open Test Point CSV"
		self.openPointsBtn["command"] = self.open_points_file
		self.openPointsBtn["bg"] = "light blue"
		self.openPointsBtn["fg"] = "black"
		self.openPointsBtn["width"] = self.widgetWidths
		self.openPointsBtn.pack(fill="x", side="top", expand=True)
		# self.openPointsBtn.grid(row=0,column=0,padx=5,pady=10,sticky=tk.E+tk.W)
		
		self.selectPointsBtn = tk.Button(self, text="Start Point Select", bg="light blue", state=tk.DISABLED)
		self.selectPointsBtn["command"] = self.start_picking
		self.selectPointsBtn["width"] = self.widgetWidths
		# self.selectPointsBtn.grid(row=1,column=0,padx=5,pady=10,sticky=tk.E+tk.W)
		self.selectPointsBtn.pack(fill="x", side="top", expand=True)
		
		self.currentTestPointsLabel = tk.Label(self, text="Point File: ")
		self.currentTestPointsLabel.pack(side="top")
		
		self.pointScrollBar = tk.Scrollbar(self)
		self.pointListBox = tk.Listbox(self)
		self.pointListBox["height"] = 30
		self.pointListBox["width"] = self.widgetWidths
		self.pointListBox["fg"] = "black"
		self.pointListBox["selectbackground"] = "#d8e7ff"
		self.pointListBox["selectforeground"] = "black"
		self.pointListBox["activestyle"] = "none"
		# self.pointListBox.grid(row=5,column=0,padx=5,pady=10,sticky=tk.E+tk.W)
		# self.pointScrollBar.pack(side="right",fill=tk.Y)
		self.pointListBox.pack(fill="both", side="bottom", expand=True)
		self.pointScrollBar.config(command=self.pointListBox.yview)
		
	
	def start_picking(self):
		confirmed = messagebox.askokcancel("Start Point Select", "Start selecting test points?")
		if confirmed is True:
			pointLine = 0
			for point in self.point_list:
				x = point[0]
				y = point[1]
				self.pointListBox.selection_clear(0, tk.END)
				self.pointListBox.selection_set(pointLine)
				self.pointListBox.see(pointLine)
				pointLine += 1
				
				# gc point selection
				pyautogui.moveTo(int(screenSizeX / 2), 0, duration)
				pyautogui.click()
				pyautogui.press('c')
				pyautogui.typewrite(x)
				pyautogui.press('tab')
				pyautogui.typewrite(y)
				pyautogui.press('enter')
				pyautogui.moveTo(int(screenSizeX / 2), int(screenSizeY / 2), duration)
				pyautogui.click()

				'''
				nextPoint = messagebox.askyesno("Confirm Selection","Select next point?")
				if nextPoint is False:
					messagebox.showinfo("Canceled","Canceling point selection")
					break
				'''

			messagebox.showinfo("Complete", "Done selecting test points")
			self.pointListBox.selection_clear(0, tk.END)
			
	def open_points_file(self):
		filename = ''
		canceled = False
		while '.csv' not in filename:
			# Tk().withdraw()
			filename = filedialog.askopenfilename()
			if '.csv' not in filename:
				retry = messagebox.askretrycancel("Failed", "Not a .csv file\nMake a new selection?")
				if retry is False:
					canceled = True
					break
			else:
				break

		if not canceled:
			self.currentTestPointFile.set(filename)
			self.currentTestPointsLabel["text"] = self.currentTestPointFile.get()
			self.currentTestPointsLabel["background"] = "#d3ffbc"
			with open(filename, 'r') as testfile:
				reader = csv.reader(testfile)
				self.point_list = list(reader)
		
			self.pointListBox.delete(0, tk.END)
			pointCounter = 1
			for point in self.point_list:
				x = point[0]
				y = point[1]
				self.pointListBox.insert(tk.END, "P" + str(pointCounter) + ": " + x + "," + y)
				pointCounter += 1
				
			if len(self.point_list) != 0:
				self.selectPointsBtn.config(state="normal")
				if len(self.point_list) > 30:
					self.pointListBox.pack_forget()
					self.pointScrollBar.pack(side="right", fill=tk.Y)
					self.pointListBox.pack(fill="both", side="bottom", expand=True)
				else:
					self.pointScrollBar.pack_forget()
					


root = tk.Tk()
app = Application(master=root)
app.mainloop()
