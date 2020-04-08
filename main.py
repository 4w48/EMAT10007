'''Startup module for the score card'''
import tkinter 
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Notebook
from tkinter.font import Font, BOLD

class Window(Tk):
	'''Window class pretty much self explanatory'''

	def __init__(self):
		super().__init__()
		self.title('Cricket Score Card')
		self.geometry('1024x800')
		self.resizable(0, 0)
		# creating a tabbed interface
		self.notebook = Notebook(self)
		self.teamA_Tab = Team(self.notebook, 'Team A')
		self.teamB_Tab = Team(self.notebook, 'Team B')
		self.notebook.add(self.teamA_Tab, text='Team A')
		self.notebook.add(self.teamB_Tab, text='Team B')
		self.notebook.pack(fill=BOTH, expand=1)

class Team(Frame):
	'''Frame representing a single team'''

	def __init__(self, master, name):
		super().__init__(master, bg='light blue')
		# creating two seperate frames for each tab and packing them onto the interface using pack functionality
		font = Font(family="Helvetica", size=40, weight=BOLD)
		self.title = Entry(self, bg='light blue', fg='black', relief=RAISED, justify=CENTER, font=font)
		self.title.insert(0, name)
		self.title.pack(side=TOP, fill=BOTH)
		self.batting_table = Table(self, 'Strike Rate', 'Batting', 'Batsman {}', 100)
		self.bowling_table = Table(self, 'Economy', 'Bowling', 'Bowler {} (W)', 6)
		self.batting_table.pack(side=LEFT)
		self.bowling_table.pack(side=RIGHT)

class Table(Frame):
	'''Class to implement batting table'''

	def __init__(self, master, calc_text, title, text, factor, padx=5):
		super().__init__(master, padx=padx, bg='light blue', borderwidth=2, relief='raised')
		# naming labels and packing them onto the interface using grid functionality
		self.title = Label(self, text=title, bg='white', fg='black')
		self.title.grid(row=1, column=1, columnspan=4)
		self.factor = factor
		name = Label(self, text='Name', pady=5, bg='light blue', fg='black')
		runs = Label(self, text='Runs', pady=5, bg='light blue', fg='black')
		balls = Label(self, text='Balls', pady=5, bg='light blue', fg='black')
		name.grid(row=2, column=1)
		runs.grid(row=2, column=2)
		balls.grid(row=2, column=3)
		calculation = Label(self, text=calc_text, pady=5, bg='light blue', fg='black')
		calculation.grid(row=2, column=4)
		# setting up batting and bowling lineups as a list and then using a for loop to systematically display entries as per the order
		self.lineup = []
		for index in range(11):
			self.lineup.append(Stats(self, index+1, text.format(index+1), factor))
		name = Label(self, text='Total', bg='light blue', fg='black')
		self.runs = IntVar(self)
		runs = Label(self, textvar=self.runs, bg='light blue', fg='black')
		self.balls = IntVar(self)
		balls = Label(self, textvar=self.balls, bg='light blue', fg='black')
		self.calculation = IntVar(self)
		calculation = Label(self, textvar=self.calculation, bg='light blue', fg='black')
		name.grid(row=14, column=1)
		runs.grid(row=14, column=2)
		balls.grid(row=14, column=3)
		calculation.grid(row=14, column=4)

	def calculate(self):
		runs, balls, calculation = 0, 0, 0
		for player in self.lineup:
                        # using the get functionality to get value of entries entered by user
			player_runs = player.runs.get()
			player_balls = player.balls.get()
			player_calc = player.calculation.get()
			# easier way to avoid any cell if no data given
			if not player_balls:
				player_balls = '0'
			if not player_calc:
				player_calc = '0'
			if not player_runs:
				player_runs = '0'
			# calculation of runs and balls to be totalled 
			runs += int(player_runs)
			balls += int(player_balls)
		self.runs.set(runs)
		self.balls.set(balls)
		if balls:
			self.calculation.set(round((runs / balls) * self.factor, 2))

class Stats():
	'''Class of widgets to be displayed in a single row and helping functions'''


	stat = ['master', 'name', 'factor', 'runs', 'balls', 'calculation', 'calculation_label']
	

	def __init__(self, master, index, text, factor):
		self.master = master
		# helping functions that are binded to achieve the calculating functionality packed onto the interface using grid functionality
		self.name = Entry(master, bg='light blue', fg='black')
		self.name.insert(0, text)
		self.factor = factor
		self.runs = Entry(master, bg='white', fg='black')
		self.balls = Entry(master, bg='white', fg='black')
		self.calculation = IntVar(master)
		self.calculation.set(0)
		self.calculation_label = Label(master, textvar=self.calculation, padx=10, bg='light blue', fg='black')
		self.name.grid(row=index+2, column=1, pady=2)
		self.runs.grid(row=index+2, column=2, pady=2)
		self.balls.grid(row=index+2, column=3, pady=2)
		self.calculation_label.grid(row=index+2, column=4, pady=2)
		self.runs.bind('<Leave>', self.calculate)
		self.balls.bind('<Leave>', self.calculate)

	def calculate(self, _):
		'''Function to calculate strikerate or economy'''

                # easier way to avoid any cell if no data given
		runs = self.runs.get()
		if not runs:
			runs = '0'
		# easier way to avoid any cell if no data given
		balls = self.balls.get()
		if not balls:
			balls = '0'
		if balls != '0':
			self.calculation.set(round((int(runs) / int(balls)) * self.factor, 2))
		self.master.calculate()

Window().mainloop()
