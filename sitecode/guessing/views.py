from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from guessing.models import Matchselect

def index(request):
    latest_question_list = Matchselect.objects.order_by('-match_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'guessing/index.html', context)
	
def detail(request, matchselect_id):
	matchselect = get_object_or_404(Matchselect, pk=matchselect_id)
	return render(request, 'guessing/detail.html', {'matchselect': matchselect})
	
def results(request, matchselect_id):
	response = "Results of match %s."
	return HttpResponse(response % matchselect_id)
	
def vote(request, matchselect_id):
	return HttpResponse("You're voting on match %s." % matchselect_id)