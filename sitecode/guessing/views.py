from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("Hello world~")
	
def detail(request, matchselect_id):
	return HttpResponse("Selected match: %s." % matchselect_id)
	
def results(request, matchselect_id):
	response = "Results of match %s."
	return HttpResponse(response % matchselect_id)
	
def vote(request, matchselect_id):
	return HttpResponse("You're voting on match %s." % matchselect_id)