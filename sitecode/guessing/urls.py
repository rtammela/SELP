from django.conf.urls import patterns, url

from guessing import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<matchselect_id>\d+)/$', views.detail, name='detail'),
	url(r'^(?P<matchselect_id>\d+)/results/$', views.results, name='results'),
	url(r'^(?P<matchselect_id>\d+)/vote/$', views.vote, name='vote'),
	url(r'^profile/(?P<username>\w+)/$',views.profile, name='profile'),
)