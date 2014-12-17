from django.contrib import admin
from guessing.models import Matchselect, Matchchoice, Matchresult

class ResultInline(admin.TabularInline):
	model = Matchresult
	extra = 1
	
class MatchAdmin(admin.ModelAdmin):
	list_display = ('game', 'match_date', 'team1', 'team2', 'creator')
	list_filter = ['match_date']
	fieldsets = [
		(None,	{'fields': ['game', 'match_date']}),
		('Teams', {'fields': ['team1', 'team2']})
	]
	inlines = [ResultInline]

admin.site.register(Matchselect, MatchAdmin)
<<<<<<< HEAD
admin.site.register(Userpoints, PointsAdmin)
=======
>>>>>>> parent of b54ba86... added admin interface to manage users' points & votes (just in case ever necessary)
