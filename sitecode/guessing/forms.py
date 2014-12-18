from django.contrib.auth.models import User
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from guessing.models import Matchselect, Matchchoice
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import datetime
from django.utils import timezone
			
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'email', 'password')
		
class MatchForm(forms.ModelForm):
	# Game name and team names must be alphanumeric, containing at least one alphabetical character:
	alphanumeric = RegexValidator(r'^(([0-9a-zA-Z])*[a-zA-Z]([0-9a-zA-Z])*)*$', 'Game name must be alphanumeric.')
	game = forms.CharField(max_length=200, validators=[alphanumeric])
	team1 = forms.CharField(max_length=50, validators=[alphanumeric])
	team2 = forms.CharField(max_length=50, validators=[alphanumeric])
	# SelectDateWidget ensures year cannot be in past
	match_date = forms.DateField(widget=SelectDateWidget, initial=timezone.now())
	
	def clean(self):
		t1 = self.cleaned_data['team1']
		t2 = self.cleaned_data['team2']
		if (t1 == t2):
			raise forms.ValidationError('The same team cannot be playing on both sides.')
		return self.cleaned_data

	def clean_match_date(self):
		date = self.cleaned_data['match_date']
		if (date < datetime.date.today()):
			raise forms.ValidationError('The match date cannot be in the past.')
		return date

	class Meta:
		model = Matchselect
		# Creator not inputted within form
		exclude = ['creator']
		fields = ('game', 'team1', 'team2', 'match_date')
