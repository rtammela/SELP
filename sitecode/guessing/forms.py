from django.contrib.auth.models import User
from django import forms
from guessing.models import Matchselect, Matchchoice

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		
class MatchForm(forms.ModelForm):
	game = forms.CharField(max_length=200, help_text='The game the match is played in')
	team1 = forms.CharField(max_length=50, help_text='Team 1')
	team2 = forms.CharField(max_length=50, help_text='Team 2')
	match_date = forms.DateTimeField()
	
	class Meta:
		model = Matchselect
		fields = ('game', 'team1', 'team2', 'match_date')