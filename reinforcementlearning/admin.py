from django.contrib import admin
from reinforcementlearning.models import GameBoard

# Register your models here.
admin.site.register(GameBoard)

class GameBoardAdmin(admin.ModelAdmin):
	model = GameBoard
	list_display = ('name')