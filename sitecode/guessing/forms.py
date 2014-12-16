from django.contrib.auth.models import User
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from guessing.models import Matchselect, Matchchoice

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		
class MatchForm(forms.ModelForm):
	game = forms.CharField(max_length=200)
	team1 = forms.CharField(max_length=50)
	team2 = forms.CharField(max_length=50)
	match_date = forms.DateField(widget=SelectDateWidget)
	
	class Meta:
		model = Matchselect
		# Creator not inputted within form
		exclude = ['creator']
		fields = ('game', 'team1', 'team2', 'match_date')