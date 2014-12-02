from django.db import models

# Create your models here.

class Matchselect(models.Model):
	match_info = models.CharField(max_length=200)
	pub_date = models.DateTimeField('data published')
	def __str__(self):
		return self.match_info
	
class Matchchoice(models.Model):
	# Match choice must come from the match choice from Matchselect
	match = models.ForeignKey(Matchselect)
	winner_choice = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)
	def __str__(self):
		return self.winner_choice