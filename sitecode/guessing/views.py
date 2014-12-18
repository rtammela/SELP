from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from django.utils import timezone
from django.db.models import Q
from guessing.forms import UserForm, MatchForm
import datetime
import itertools

from guessing.models import Matchselect, Matchchoice, Matchresult, Uservotes, Userpoints

# Common information (user leaderboard, browsing by game/team) used by all pages
def match_browse_info():
	# List of games for which matches exist:
	games = Matchselect.objects.distinct().values_list('game',flat=True)
	# List of teams participating in any matches for any games:
	teams = Matchselect.objects.distinct().values_list('team1','team2')
	tlist = []
	for t1,t2 in teams:
		if t1 not in tlist:
			tlist.append(t1)
		if t2 not in tlist:
			tlist.append(t2)
	# List of users sorted by points:
	users = Userpoints.objects.order_by('-points')[:10]
	accuracies = []
	for u in users:
		correct = u.points
		total = u.votescompleted
		if total > 0:
			correct_rate = (float(correct)/float(total))*100
		else:
			correct_rate = 0
		accuracies.append(correct_rate)
	browse_users = zip(users,accuracies)
	context = {'browse_games' : games, 'browse_teams' : tlist, 'browse_users' : browse_users}
	return context

def index(request):
	match_browse = match_browse_info()
	# 10 latest matches:
	latest_question_list = Matchselect.objects.order_by('-match_date')[:10]
	context = {'latest_question_list' : latest_question_list, 'match_browse' : match_browse}
	return render(request, 'guessing/index.html', context)
	
def games(request, game):
	match_browse = match_browse_info()
	game_matches = Matchselect.objects.filter(game=game)
	context = {'game_matches' : game_matches, 'match_browse' : match_browse}
	return render(request, 'guessing/games.html', context)
	
def teams(request, teams):
	
	match_browse = match_browse_info()
	# Get list of all matches where the team has participated
	game_matches = Matchselect.objects.filter( Q(team1=teams) | Q(team2=teams))
	game_matches.order_by('-match_date')
	# Calculate winrate for team 
	matches_won = 0
	total_matches = 0
	team_name1 = game_matches[0]
	if team_name1.team1 == teams:
		team_name = team_name1.team1
	else:
		team_name = team_name1.team2
	for g in game_matches:
		total_matches += 1
		match_win = Matchresult.objects.filter(match=g,winner=teams)
		if match_win:
			matches_won +=1
	win_rate = (float(matches_won)/float(total_matches))*100
	context = {'game_matches' : game_matches, 'team_name' : team_name, 'win_rate' : win_rate, 'match_browse' : match_browse}
	return render(request, 'guessing/teams.html',context)
	
def detail(request, matchselect_id):
	match_browse = match_browse_info()
	matchselect = get_object_or_404(Matchselect, pk=matchselect_id)
	matchresult = Matchresult.objects.filter(match=matchselect_id)
	# Check if user (if any are logged in) has already voted in this poll:
	if request.user.is_authenticated():
		voters = [v.voter for v in Uservotes.objects.filter(match=matchselect)]
		u = User.objects.get(username=request.user.username)
		# If so, take user directly to results page
		if u in voters:
			context = {'matchselect': matchselect, 'matchresult' : matchresult, 'match_browse' : match_browse, 'votepercents' : get_votepercents(matchselect_id)}
			return render(request, 'guessing/results.html', context)
	# Check if match has completed:
	if matchselect.match_date < datetime.date.today():
		context = {'matchselect': matchselect, 'matchresult' : matchresult, 'match_browse' : match_browse, 'error_message': 'Match has closed.'}
		return render( request, 'guessing/results.html', context)
	# Otherwise, let user vote in the poll
	context = {'matchselect': matchselect, 'match_browse' : match_browse, 'votepercents' : get_votepercents(matchselect_id)}
	return render(request, 'guessing/detail.html', context)
	
# Calculations of vote percentages for a given match
def get_votepercents(matchselect_id):
	matchselect = get_object_or_404(Matchselect, pk=matchselect_id)
	matchresult = Matchresult.objects.filter(match=matchselect_id)
	# % of votes for each team:
	t1_win = matchselect.team1
	t2_win = matchselect.team2
	t1_choice = Matchchoice.objects.filter(match=matchselect_id,winner_choice=t1_win)
	t1_votes = 0
	for t in t1_choice:
		t1_votes = t.votes
	t2_choice = Matchchoice.objects.filter(match=matchselect_id,winner_choice=t2_win)
	t2_votes = 0
	for t in t2_choice:
		t2_votes = t.votes
	if (t1_votes + t2_votes) > 0:
		t1_percent = float(t1_votes) / float(t1_votes+t2_votes) * 100
		t2_percent = float(t2_votes) / float(t1_votes+t2_votes) * 100
	else:
		t1_percent = 0
		t2_percent = 0
	votepercents1 = [t1_win,t1_votes,t1_percent]
	votepercents2 = [t2_win,t2_votes,t2_percent]
	votepercents = [votepercents1,votepercents2]
	return votepercents
	
def results(request, matchselect_id):
	match_browse = match_browse_info()
	matchselect = get_object_or_404(Matchselect, pk=matchselect_id)
	matchresult = Matchresult.objects.filter(match=matchselect_id)
	context = {'matchselect': matchselect, 'matchresult' : matchresult, 'votepercents' : get_votepercents(matchselect_id), 'match_browse' : match_browse}
	return render(request, 'guessing/results.html', context)
	
def vote(request, matchselect_id):
	match_browse = match_browse_info()
	p = get_object_or_404(Matchselect, pk=matchselect_id)
	try:
		selected_choice = p.matchchoice_set.get(pk=request.POST['matchchoice'])
	except (KeyError, Matchchoice.DoesNotExist):
		# Redisplay the question voting form if no winner_choice selected
		context = {'matchselect': p, 'match_browse' : match_browse, 'error_message': "You didn't select a choice.",}
		return render(request, 'guessing/detail.html', context)
	else:
		# Only logged in users can vote
		if request.user.is_authenticated():
			u = User.objects.get(username=request.user.username)
			# Save user vote choice,
			user_vote = Uservotes(voter=u,match=p,winner_choice=selected_choice)
			user_vote.save()
			# Increment vote counter for specific choice,
			selected_choice.votes += 1
			selected_choice.save()
			# Increment total number of votes for that user.
			vote_count = Userpoints.objects.filter(voter=u)
			if vote_count:
				for v in vote_count:
					v.totalvotes += 1
					v.save()
			else:
				v = Userpoints(voter=u,totalvotes=1,points=0,votescompleted=0)
				v.save()
			# Always return an HttpResponseRedirect after successfully dealing
			# with POST data. This prevents data from being posted twice if a
			# user hits the Back button.
			return HttpResponseRedirect(reverse('results', args=(p.id,)))
		else:
			return HttpResponse('Must be logged in to vote')

def profile(request, username):
	match_browse = match_browse_info()
	try:
		u = User.objects.get(username=username)
	except (KeyError, User.DoesNotExist):
		latest_question_list = Matchselect.objects.order_by('-match_date')[:10]
		games = Matchselect.objects.distinct().values_list('game',flat=True)
		context = {'error_message' : 'User by that name does not exist.', 'latest_question_list' : latest_question_list, 'games' : games, 'match_browse' : match_browse}
		return render(request, 'guessing/index.html', context )
	else:
		# User's winner_choice of all matches where user has voted are fetched:
		uvotes = Uservotes.objects.filter(voter=u).values()
		# User's vote point details gathered:
		p = Userpoints.objects.filter(voter=u)
		# Matches created by user gathered:
		matches_created = Matchselect.objects.filter(creator=u)
		correct_rate=0
		if not p:
			p = Userpoints(voter=u,totalvotes=0,points=0)
			p.save()
			correct = 0
			total = 0
			# Accuracy for user calculated: Must use for loop ('p' is a QuerySet, which cannot be accessed direcly (e.g. p.points), and may be empty, in which case initialise to 0)
		else:
			for x in p:
				correct = x.points
				total = x.votescompleted
				if total > 0:
					correct_rate = (float(correct)/float(total))*100
		gamesvoted = Uservotes.objects.filter(voter=u).values_list('match_id', flat=True)
		# Match details of the corresponding matches are fetched, if user voted in any games:
		if not gamesvoted:
			voteinfolist = []
		else:
			gameinfo = []
			for i in gamesvoted:
				a = Matchselect.objects.filter(pk=i)
				gameinfo.append(a)
			# Winner_choice is paired with match details for each match voted in:
			voteinfolist = zip(uvotes,gameinfo)
		context = {'u': u, 'voteinfolist' : voteinfolist, 'p' : p, 'matches_created' : matches_created, 'correct_rate' : correct_rate, 'match_browse' : match_browse}
		return render(request, 'guessing/profile.html', context)
		
def register(request):
	match_browse = match_browse_info()
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
	return render_to_response('guessing/register.html',{'user_form' : user_form,'registered' : registered,'match_browse' : match_browse},context)
		
def user_login(request):
	match_browse = match_browse_info()
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
			return render(request,'guessing/login.html', {'error_message': 'Incorrect login details.',})
	else:
		return render_to_response('guessing/login.html', {'match_browse' : match_browse}, context)
		
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/guessing/')
	
def add_match(request):
	match_browse = match_browse_info()
	# First checks if user is logged in
	if not request.user.is_authenticated():
		context = {'match_browse' : match_browse, 'error_message': "You must be logged in to create a new match.",}
		return render(request, 'guessing/add_match.html', context)
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
	return render_to_response('guessing/add_match.html', {'match_form' : match_form, 'match_browse' : match_browse}, context)
	
@permission_required('guessing.add_userpoints')
def add_winner(request, matchselect_id):
	match_browse = match_browse_info()
	p = get_object_or_404(Matchselect, pk=matchselect_id)
	winner_exists = Matchresult.objects.filter(match=p)
	if winner_exists:
		context = {'matchselect': p, 'match_browse' : match_browse,'error_message': "Winner has already been added.",}
		return render(request, 'guessing/results.html', context )
	try:
		selected_choice = p.matchchoice_set.get(pk=request.POST['matchchoice'])
	except (KeyError, Matchchoice.DoesNotExist):
		# Redisplay the question voting form if no winner_choice selected
		context = {'matchselect': p, 'match_browse' : match_browse,'error_message': "You didn't select a winner.",}
		return render(request, 'guessing/add_winner.html', context)
	else:
		w = Matchresult(match=p,winner=selected_choice)
		w.save()
		# Go through all users who voted in this match
		voters = Uservotes.objects.filter(match=p)
		for v in voters:
			votercount = Userpoints.objects.get(voter=v.voter)
			votercount.votescompleted += 1
			votercount.save()
			# If the user voted for the winner, increment points by 1:
			if v.winner_choice == str(selected_choice):
				voterpoints = Userpoints.objects.get(voter=v.voter)
				voterpoints.points += 1
				voterpoints.save()
		return HttpResponseRedirect(reverse('results', args=(p.id,)))
