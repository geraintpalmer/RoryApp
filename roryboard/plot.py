import matplotlib.pyplot as plt, mpld3
from csv import reader

class Data:
	"""
	A class to hold the data and plot it
	"""
	def __init__(self, x, y):
		"""
		Initialises the class
		"""
		self.x = x
		self.y = y
		self.data = {}

	def import_csv(self, name, directory):
		"""
		Imports the csv file
		"""
		data_file = open('%s/%s.csv' % (directory, name), 'r')
		rdr = reader(data_file)
		for row in rdr:
			self.data[row[0]] = row[1:]
		data_file.close()

	def create_graph(self, num_eps):
		"""
		Plots Q against time for a specific state-action pair
		"""
		fig, ax = plt.subplots()
		box = ax.get_position()
		plt.plot(self.data[str((int(self.x), int(self.y), 'North'))], color='b', label='North')
		plt.plot(self.data[str((int(self.x), int(self.y), 'East'))], color='g', label='East')
		plt.plot(self.data[str((int(self.x), int(self.y), 'South'))], color='r', label='South')
		plt.plot(self.data[str((int(self.x), int(self.y), 'West'))], color='y', label='West')
		ax.legend(loc='mouse', title='')
		plt.xlabel('Episodes')
		plt.ylabel('Q-Values')
		plt.hlines(y=0, xmin=0, xmax=num_eps)
		self.graph = mpld3.fig_to_html(fig)