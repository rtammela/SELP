from django.contrib import admin
from guessing.models import Matchselect, Matchchoice, Matchresult, Userpoints

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

class PointsAdmin(admin.ModelAdmin):
	list_display = ('voter', 'totalvotes', 'points')
	list_filter = ['points']
	
admin.site.register(Matchselect, MatchAdmin)
admin.site.register(Userpoints, PointsAdmin)