from django.conf.urls import patterns, url

from guessing import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
)