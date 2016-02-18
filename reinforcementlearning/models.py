from django.db import models
from django.forms import ModelForm

# Create your models here.
class GameBoard(models.Model):
	name = models.CharField(max_length=60)
	grid_width = models.IntegerField()
	grid_height = models.IntegerField()
	start_x = models.IntegerField()
	start_y = models.IntegerField()
	goal_x = models.IntegerField()
	goal_y = models.IntegerField()
	death_coords = models.TextField()
	number_of_episodes = models.IntegerField()
	learning_rate = models.FloatField()
	discount_rate = models.FloatField()
	action_selection_parameter = models.FloatField()
	success_rate = models.FloatField()
	move_cost = models.FloatField()
	death_cost = models.FloatField()
	goal_reward = models.FloatField()
	standard_set = models.NullBooleanField()
	slug = models.SlugField(unique=True)
	