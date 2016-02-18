from django import forms

from .models import GameBoard

class GameBoardForm(forms.ModelForm):

    class Meta:
        model = GameBoard
        fields = ('name', 'grid_width', 'grid_height', 'start_x', 'start_y', 'goal_x', 'goal_y', 'death_coords', 'number_of_episodes', 'learning_rate', 'discount_rate', 'action_selection_parameter', 'success_rate', 'move_cost', 'death_cost', 'goal_reward', 'standard_set', 'slug',)