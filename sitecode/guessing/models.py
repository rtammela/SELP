from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Matchselect(models.Model):
	game = models.CharField(max_length=200)
	team1 = models.CharField(max_length = 50)
	team2 = models.CharField(max_length = 50)
	match_date = models.DateTimeField('date of match')
	creator = models.ForeignKey(User)
	def __str__(self):
		return self.game
	
class Matchchoice(models.Model):
	# Match choice must come from the match choice from Matchselect
	match = models.ForeignKey(Matchselect)
	winner_choice = models.CharField(max_length=50)
	votes = models.IntegerField(default=0)
	def __str__(self):
		return self.winner_choice
		
class Matchresult(models.Model):
	match = models.ForeignKey(Matchselect)
	winner = models.CharField(max_length=50)
	def __str__(self):
		return self.winner
		
class Uservotes(models.Model):
	voter = models.ForeignKey(User)
	match = models.ForeignKey(Matchselect)
	winner_choice = models.CharField(max_length=50)
	def __str__(self):
		return self.winner_choice