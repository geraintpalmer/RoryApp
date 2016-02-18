from django.shortcuts import render, get_object_or_404, redirect
from roryboard.board import *
from roryboard.plot import *
from reinforcementlearning.models import GameBoard
from .forms import GameBoardForm
import os


# Create your views here.
def index(request):
	# this is your view
	gameboards = GameBoard.objects.all()
	return render(request, 'index.html', {
		'gameboards': gameboards
		})


def theboard(request, slug):

	gameboard = get_object_or_404(GameBoard, slug=slug)

	board_dimentions = [gameboard.grid_width, gameboard.grid_height]
	start_pos = [gameboard.start_x, gameboard.start_y]
	goal_pos = [gameboard.goal_x, gameboard.goal_y]
	deaths = eval(gameboard.death_coords)
	death_poss = {'Death '+str(i+1):deaths[i] for i in range(len(deaths))}
	BoardGame = Board(board_dimentions, start_pos, goal_pos, gameboard.number_of_episodes, gameboard.learning_rate, gameboard.discount_rate, gameboard.action_selection_parameter, gameboard.success_rate, death_poss, gameboard.move_cost, gameboard.death_cost, gameboard.goal_reward)	

	return render(request, 'theboard.html', {
		'gameboard':gameboard,
		'BoardGame':BoardGame
		})


def results(request, slug):

	gameboard = get_object_or_404(GameBoard, slug=slug)

	board_dimentions = [gameboard.grid_width, gameboard.grid_height]
	start_pos = [gameboard.start_x, gameboard.start_y]
	goal_pos = [gameboard.goal_x, gameboard.goal_y]
	deaths = eval(gameboard.death_coords)
	death_poss = {'Death '+str(i+1):deaths[i] for i in range(len(deaths))}
	BoardGame = Board(board_dimentions, start_pos, goal_pos, gameboard.number_of_episodes, gameboard.learning_rate, gameboard.discount_rate, gameboard.action_selection_parameter, gameboard.success_rate, death_poss, gameboard.move_cost, gameboard.death_cost, gameboard.goal_reward)	
	
	back_to_this_page = "../" + gameboard.slug + "/results"
	BoardGame.simulate()
	dr = os.getcwd()
	BoardGame.write_time_series_to_file(gameboard.slug, dr+'/reinforcementlearning/static')
	start_x = str(gameboard.start_x)
	start_y = str(gameboard.start_y)

	return render(request, 'results.html', {
		'gameboard':gameboard,
		'BoardGame':BoardGame,
		'back_to_this_page':back_to_this_page,
		'start_x':start_x,
		'start_y':start_y
		})


def boardlist(request):
	# this is your view
	gameboards = GameBoard.objects.all()
	return render(request, 'boardlist.html', {
		'gameboards': gameboards
		})



def learninggraphs(request, slug, col, row):

	gameboard = get_object_or_404(GameBoard, slug=slug)
	data = Data(col, row)
	dr = os.getcwd()
	data.import_csv(gameboard.slug, dr+'/reinforcementlearning/static')
	data.create_graph(gameboard.number_of_episodes)

	return render(request, 'learninggraphs.html', {
		'col':col,
		'row':row,
		'data':data
		})


def createboard(request):
    if request.method == "POST":
        form = GameBoardForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            slug = post.slug
            post.save()
            return redirect('theboard', {'slug':slug}, pk=post.pk)
    else:
        form = GameBoardForm()
    return render(request, 'createboard.html', {'form':form})
