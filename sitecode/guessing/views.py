from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from guessing.models import Matchselect

def index(request):
    latest_question_list = Matchselect.objects.order_by('-pub_date')[:5]
    template = loader.get_template('guessing/index.html')
    context = RequestContext(request, {
        'latest_question_list': latest_question_list,
    })
    return HttpResponse(template.render(context))
	
def detail(request, matchselect_id):
	return HttpResponse("Selected match: %s." % matchselect_id)
	
def results(request, matchselect_id):
	response = "Results of match %s."
	return HttpResponse(response % matchselect_id)
	
def vote(request, matchselect_id):
	return HttpResponse("You're voting on match %s." % matchselect_id)