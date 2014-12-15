from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from guessing.models import Matchselect, Matchchoice, Matchresult, Uservotes

def index(request):
    latest_question_list = Matchselect.objects.order_by('-match_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'guessing/index.html', context)
	
def detail(request, matchselect_id):
	matchselect = get_object_or_404(Matchselect, pk=matchselect_id)
	return render(request, 'guessing/detail.html', {'matchselect': matchselect})
	
def results(request, matchselect_id):
	matchselect = get_object_or_404(Matchselect, pk=matchselect_id)
	return render(request, 'guessing/results.html', {'matchselect': matchselect})
	
def vote(request, matchselect_id):
    p = get_object_or_404(Matchselect, pk=matchselect_id)
    try:
        selected_choice = p.matchchoice_set.get(pk=request.POST['matchchoice'])
    except (KeyError, Matchchoice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'guessing/detail.html', {
            'matchselect': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', args=(p.id,)))

def profile(request, username):
	u = User.objects.get(username=username)
	uvotes = Uservotes.objects.filter(voter=u).values()
	games = Uservotes.objects.filter(voter=u).values_list('match_id', flat=True)
	gameinfo = []
	for i in games:
		a = Matchselect.objects.filter(pk=i)
		gameinfo.append(a)
	voteinfolist = zip(uvotes,gameinfo)
	return render(request, 'guessing/profile.html', {
		'u': u,
		'voteinfolist' : voteinfolist
		})