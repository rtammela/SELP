from django.contrib import admin
from guessing.models import Matchselect, Matchchoice, Matchresult

class ResultInline(admin.StackedInline):
	model = Matchresult
	extra = 1
	
class MatchAdmin(admin.ModelAdmin):
	inlines = [ResultInline]

admin.site.register(Matchselect, MatchAdmin)
