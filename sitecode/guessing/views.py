from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from django.utils import timezone
from guessing.forms import UserForm, MatchForm

from guessing.models import Matchselect, Matchchoice, Matchresult, Uservotes, Userpoints

def index(request):
	latest_question_list = Matchselect.objects.order_by('-match_date')[:10]
	context = {'latest_question_list': latest_question_list}
	return render(request, 'guessing/index.html', context)
	
def detail(request, matchselect_id):
	matchselect = get_object_or_404(Matchselect, pk=matchselect_id)
	# Check if user (if any are logged in) has already voted in this poll:
	if request.user.is_authenticated():
		voters = [v.voter for v in Uservotes.objects.filter(match=matchselect)]
		u = User.objects.get(username=request.user.username)
		# If so, take user directly to results page
		if u in voters:
			return render(request, 'guessing/results.html', {'matchselect': matchselect})
	# Check if match has completed:
	if matchselect.match_date < timezone.now():
		return render( request, 'guessing/results.html', {'matchselect': matchselect, 'error_message': 'Match has closed.'})
	# Otherwise, let user vote in the poll
	return render(request, 'guessing/detail.html', {'matchselect': matchselect})
	
def results(request, matchselect_id):
	matchselect = get_object_or_404(Matchselect, pk=matchselect_id)
	return render(request, 'guessing/results.html', {'matchselect': matchselect})
	
def vote(request, matchselect_id):
	p = get_object_or_404(Matchselect, pk=matchselect_id)
	try:
		selected_choice = p.matchchoice_set.get(pk=request.POST['matchchoice'])
	except (KeyError, Matchchoice.DoesNotExist):
		# Redisplay the question voting form if no winner_choice selected
		return render(
			request, 
			'guessing/detail.html', {
			'matchselect': p,
			'error_message': "You didn't select a choice.",
		})
	else:
		# Only logged in users can vote
		if request.user.is_authenticated():
			u = User.objects.get(username=request.user.username)
			user_vote = Uservotes(voter=u,match=p,winner_choice=selected_choice)
			user_vote.save()
			selected_choice.votes += 1
			selected_choice.save()
			# Always return an HttpResponseRedirect after successfully dealing
			# with POST data. This prevents data from being posted twice if a
			# user hits the Back button.
			return HttpResponseRedirect(
				reverse(
				'results', 
				args=(p.id,)))
		else:
			return HttpResponse('Must be logged in to vote')

def profile(request, username):
	# User's winner_choice of all matches where user has voted are fetched:
	u = User.objects.get(username=username)
	uvotes = Uservotes.objects.filter(voter=u).values()
	games = Uservotes.objects.filter(voter=u).values_list('match_id', flat=True)
	# Match details of the corresponding matches are fetched:
	gameinfo = []
	for i in games:
		a = Matchselect.objects.filter(pk=i)
		gameinfo.append(a)
	# Winner_choice is paired with match details for each match voted in:
	voteinfolist = zip(uvotes,gameinfo)
	p = Userpoints.objects.filter(voter=u)
	if not p:
		p = Userpoints(voter=u,totalvotes=0,points=0)
		p.save()
	return render(
		request, 'guessing/profile.html', {
		'u': u,
		'voteinfolist' : voteinfolist,
		'p' : p
		})
		
def register(request):
	context = RequestContext(request)
	registered = False
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)		
		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()
			registered = True
		else:
			print(user_form.errors)
	else:
		user_form = UserForm()
	return render_to_response(
		'guessing/register.html',{
		'user_form' : user_form,
		'registered' : registered
		},context)
		
def user_login(request):
	context = RequestContext(request)
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/guessing/') 
			else:
				return HttpResponse('This account is not active.')
		else:
			return render(
			request,
			'guessing/login.html', {
			'error_message': 'Incorrect login details.',
			})
	
	else:
		return render_to_response('guessing/login.html', {}, context)
		
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/guessing/')
	
def add_match(request):
	# First checks if user is logged in
	if not request.user.is_authenticated():
		return render(
			request, 
			'guessing/add_match.html', {
			'error_message': "You must be logged in to create a new match.",
		})
	context = RequestContext(request)
	u = User.objects.get(username=request.user.username)
	if request.method == 'POST':
		match_form = MatchForm(request.POST)
		if match_form.is_valid():
			# Temporarily saves form with data inputted by user, then saves form with the user as the creator of the match
			f = match_form.save(commit=False)
			newmatch = Matchselect(game=f.game,team1=f.team1,team2=f.team2,match_date=f.match_date,creator=u)
			newmatch.save()
			# Creates set of match choices based on team1 and team2.
			newmatch.matchchoice_set.create(winner_choice=f.team1,votes='0')
			newmatch.matchchoice_set.create(winner_choice=f.team2,votes='0')
			return render(request, 'guessing/detail.html', {'matchselect': newmatch})
		else:
			print(match_form.errors)
	else:
		match_form=MatchForm()
	return render_to_response('guessing/add_match.html', {'match_form' : match_form}, context)
	
@permission_required('guessing.add_userpoints')
def add_winner(request, matchselect_id):
	p = get_object_or_404(Matchselect, pk=matchselect_id)
	winner_exists = Matchresult.objects.filter(match=p)
	if winner_exists:
		return render(
			request, 
			'guessing/results.html', {
			'matchselect': p,
			'error_message': "Winner has already been added.",
		})
	try:
		selected_choice = p.matchchoice_set.get(pk=request.POST['matchchoice'])
	except (KeyError, Matchchoice.DoesNotExist):
		# Redisplay the question voting form if no winner_choice selected
		return render(
			request, 
			'guessing/add_winner.html', {
			'matchselect': p,
			'error_message': "You didn't select a choice.",
		})
	else:
		w = Matchresult(match=p,winner=selected_choice)
		w.save()
		# Go through all users who voted in this match
		voters = Uservotes.objects.filter(match=p)
		for v in voters:
			# If the user voted for the winner, increment points by 1:
			if v.winner_choice == str(selected_choice):
				voterpoints = Userpoints.objects.get(voter=v.voter)
				voterpoints.points += 1
				voterpoints.save()
		return HttpResponseRedirect(
				reverse(
				'results', 
				args=(p.id,)))
