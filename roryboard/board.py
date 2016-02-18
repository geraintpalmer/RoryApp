from __future__ import division
import docopt
import yaml
import random
from csv import writer



class Squares():
	"""
	A class which holds information about each square on the playing board
	"""
	def __init__(self, square_coords, identifier, move_cost, reward):
		"""
		Initialises the square
		"""
		self.coords = square_coords
		self.identifier = str(identifier)
		self.reward = reward
		self.move_cost = move_cost



class Robot():
	"""
	A class to hold the robot
	"""
	def __init__(self, playing_board, learning_rate, discount_rate, action_selection_parameter, success_rate):
		"""
		Initialises the robot
		"""
		self.playing_board = playing_board
		self.actions = ['North', 'East', 'South', 'West']
		self.action_selection_parameter = action_selection_parameter
		self.Vs = {sqr.coords:0 for row in self.playing_board.squares for sqr in row}
		self.Qs = Qs = {sqr.coords:{action:0 for action in self.actions} for row in self.playing_board.squares for sqr in row}
		self.moves = 0
		self.current_episode = 0
		self.coords = tuple(self.playing_board.starting_coords)
		self.learning_rate = learning_rate
		self.discount_rate = discount_rate
		self.transitions = {action:[success_rate if action==self.actions[i] else (1-success_rate)/3 for i in range(4)] for action in self.actions}
		self.movement_dict = {'North':lambda coords: (coords[0], min(coords[1]+1, self.playing_board.grid_height-1)),
								'South':lambda coords: (coords[0], max(coords[1]-1, 0)),
								'East':lambda coords: (min(coords[0]+1, self.playing_board.grid_width-1), coords[1]),
								'West':lambda coords:(max(0, coords[0]-1), coords[1])}

	def select_action(self, sqr):
		"""
		Selects which action to take using the epsilon-soft action selection policy
		"""
		rnd_num = random.random()
		if rnd_num < 1 - self.action_selection_parameter:
			return str(max(self.Qs[sqr], key=lambda x: self.Qs[sqr][x]))
		return random.choice(self.actions)

	def find_destination(self, sqr, action):
		"""
		Chooses the new coordinates after taking an action, according to the faultiness
		"""
		rnd_num = random.random()
		sum_p, indx = 0, 0
		while rnd_num > sum_p:
			direction = self.actions[indx]
			sum_p += self.transitions[action][indx]
			indx += 1
		return self.movement_dict[direction](sqr)

	def Q_Learning(self, action, reward, sqr, new_sqr):
		"""
		Updates the Q and V values
		"""	
		self.Qs[sqr][action] = (
			1-self.learning_rate)*self.Qs[sqr][action] + self.learning_rate*(
			reward + self.discount_rate*self.Vs[new_sqr]
			)
		self.Vs[sqr] = max(self.Qs[sqr].values())









class Board():
	"""
	A class which holds the playing board
	"""

	def __init__(self, board_dimentions, start_pos, goal_pos, num_eps, learning_rate, discount_rate, action_selection_parameter, success_rate, death_poss, move_cost, death_cost, goal_reward):
		"""
		Initialises the playing board
		"""
		self.grid_width = board_dimentions[0]
		self.grid_height = board_dimentions[1]
		self.starting_coords = start_pos
		self.goal_coords = goal_pos
		self.death_coords = death_poss
		self.move_cost = move_cost
		self.death_cost = death_cost
		self.goal_reward = goal_reward
		self.squares = self.create_squares()
		self.create_board()
		self.number_of_episodes = int(num_eps)
		self.robot = Robot(self, learning_rate, discount_rate, action_selection_parameter, success_rate)

	def create_squares(self):
		"""
		Creates a grid of all board squares
		"""
		sqrs = []
		for row in range(self.grid_height):
			sqrs.append([])
			for col in range(self.grid_width):
				identifier = 'Normal'
				move_cost = 0
				reward = 0
				marker = ' '
				if [col, row] == self.starting_coords:
					marker = 'S'
				if [col, row] == self.goal_coords:
					identifier = 'Goal'
					move_cost = self.move_cost
					reward = self.goal_reward
					marker = 'G'
				if any([[col, row] == coords for coords in self.death_coords.values()]):
					identifier = 'Death'
					move_cost = self.move_cost
					reward = self.death_cost
					marker = 'D'
				sqrs[row].append(Squares((col, row), identifier, move_cost, reward))
		return sqrs

	def create_board(self):
		"""
		Creates a dictionary board to show on the site
		"""
		board_dict = {i:{j:' ' for j in range(self.grid_width)} for i in range(self.grid_height)}
		board_dict[self.starting_coords[1]][self.starting_coords[0]] = 'S'
		board_dict[self.goal_coords[1]][self.goal_coords[0]] = 'G'

		for d in self.death_coords.values():
			board_dict[d[1]][d[0]] = 'D'

		self.board_dict = board_dict
		self.results_dict = board_dict
		self.board_to_show = self.create_show_board()

	def create_show_board(self):
		"""
		Creates the board in a format to show a html table of
		"""
		board_to_show = {i:{j:' ' for j in range(self.grid_width)} for i in range(self.grid_height)}
		for i in range(self.grid_height):
			for j in range(self.grid_width):
				board_to_show[i][j] = self.board_dict[self.grid_height-i-1][j]
		return board_to_show


	def simulate(self):
		"""
		Simulates many episodes of the game while the robots learns the best policies
		"""
		self.robot.Qs_time_series = {sqr.coords:{action:[] for action in self.robot.actions} for row in self.squares for sqr in row}

		while self.robot.current_episode < self.number_of_episodes:
			action = self.robot.select_action(self.robot.coords)
			new_coords = self.robot.find_destination(self.robot.coords, action)
			self.robot.moves += 1

			reward = self.squares[new_coords[1]][new_coords[0]].reward + (
				self.squares[new_coords[1]][new_coords[0]].move_cost * self.robot.moves)
			self.robot.Q_Learning(action, reward, self.robot.coords, new_coords)

			self.robot.coords = new_coords

			if (self.squares[new_coords[1]][new_coords[0]].identifier == 'Death' or
				self.squares[new_coords[1]][new_coords[0]].identifier == 'Goal'):
				self.robot.moves = 0
				self.robot.coords = tuple(self.starting_coords)
				self.robot.current_episode += 1

				for row in range(self.grid_height):
					for col in range(self.grid_width):
						for action in self.robot.actions:
							self.robot.Qs_time_series[(col, row)][action].append(self.robot.Qs[(col, row)][action])

		self.update_results()



	def update_results(self):
		"""
		Updates the table to show the optimal directions to take for each square
		"""
		for row in range(self.grid_height):
			for col in range(self.grid_width):
				if self.squares[row][col].identifier == 'Goal':
					self.results_dict[col][row] = ('G')
				elif self.squares[row][col].identifier == 'Death':
					self.results_dict[col][row] = ('D')
				elif max(self.robot.Qs[(col, row)], key=lambda x: self.robot.Qs[(col, row)][x]) == 'North':
					self.results_dict[col][row] = (u"\u2191")
				elif max(self.robot.Qs[(col, row)], key=lambda x: self.robot.Qs[(col, row)][x]) == 'East':
					self.results_dict[col][row] = (u"\u2192")
				elif max(self.robot.Qs[(col, row)], key=lambda x: self.robot.Qs[(col, row)][x]) == 'South':
					self.results_dict[col][row] = (u"\u2193")
				elif max(self.robot.Qs[(col, row)], key=lambda x: self.robot.Qs[(col, row)][x]) == 'West':
					self.results_dict[col][row] = (u"\u2190")
		self.results_to_show = self.show_results()

	def show_results(self):
		"""
		Writes a dictionary of results in the form to show in html
		"""
		results_to_show = {i:{j:' ' for j in range(self.grid_width)} for i in range(self.grid_height)}
		for i in range(self.grid_height):
			for j in range(self.grid_width):
				results_to_show[i][j] = [self.results_dict[j][self.grid_height-i-1], str(j), str(self.grid_height - i - 1)]
		return results_to_show


	def write_time_series_to_file(self, name, directory):
		"""
		Writes the time series to a yml file to plot later
		"""
		data_file = open('%s/%s.csv' % (directory, name), 'w')
		csv_wrtr = writer(data_file)
		for row in range(self.grid_height):
			for col in range(self.grid_width):
				for action in self.robot.actions:
					row_to_write = [(col, row, action)] + self.robot.Qs_time_series[(col, row)][action]
					csv_wrtr.writerow(row_to_write)
		data_file.close()




