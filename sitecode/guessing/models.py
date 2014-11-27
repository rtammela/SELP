from django.db import models

# Create your models here.

class Matchlist(models.Model):
	match_list = models.CharField(max_length=200)
	
class Matchselect(models.Model):
	match_select = models.ForeignKey(Matchlist)
	match_info = models.CharField(max_length=200)
	pub_date = models.DateTimeField('data published')
	
class Matchchoice(models.Model):
	# Match choice must come from the match choice from Matchselect
	match = models.ForeignKey(Matchselect)
	winner_choice = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)