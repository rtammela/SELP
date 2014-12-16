from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext
from guessing.forms import UserForm

from guessing.models import Matchselect, Matchchoice, Matchresult, Uservotes

def index(request):
	latest_question_list = Matchselect.objects.order_by('-match_date')[:5]
	context = {'latest_question_list': latest_question_list}
	return render(request, 'guessing/index.html', context)
	
def detail(request, matchselect_id):
	# Check if user has already voted in this poll:
	matchselect = get_object_or_404(Matchselect, pk=matchselect_id)
	voters = [v.voter for v in Uservotes.objects.filter(match=matchselect)]
	u = User.objects.get(username=request.user.username)
	# If so, take user directly to results page
	if u in voters:
		return render(request, 'guessing/results.html', {'matchselect': matchselect})
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
	return render(
		request, 'guessing/profile.html', {
		'u': u,
		'voteinfolist' : voteinfolist
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
			return HttpResponse('Incorrect login details.')
	
	else:
		return render_to_response('guessing/login.html', {}, context)
		
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/guessing/')