from django.contrib.auth.models import User
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from guessing.models import Matchselect, Matchchoice
from django.core.exceptions import ValidationError
import datetime
from django.utils import timezone
			
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		
class MatchForm(forms.ModelForm):
	game = forms.CharField(max_length=200)
	team1 = forms.CharField(max_length=50)
	team2 = forms.CharField(max_length=50)
	# SelectDateWidget ensures year cannot be in past
	match_date = forms.DateField(widget=SelectDateWidget, initial=timezone.now())

	def clean_match_date(self):
		date = self.cleaned_data['match_date']
		t = timezone.now()
		# Lengthy way of checking, but only way to compare datetime to date without errors
		if ((date.year == t.year ) and (date.month < t.month)) or ((date.year == t.year) and (date.month == t.month) and (date.day < t.day)):
			raise forms.ValidationError('The match date cannot be in the past.')
		return date
	
	class Meta:
		model = Matchselect
		# Creator not inputted within form
		exclude = ['creator']
		fields = ('game', 'team1', 'team2', 'match_date')