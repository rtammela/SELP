from django.conf.urls import patterns, url

from guessing import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^(?P<matchselect_id>\d+)/$', views.detail, name='detail'),
	url(r'^(?P<matchselect_id>\d+)/results/$', views.results, name='results'),
	url(r'^(?P<matchselect_id>\d+)/vote/$', views.vote, name='vote'),
	url(r'^(?P<matchselect_id>\d+)/add_winner/$', views.add_winner, name = 'add_winner'),
	url(r'^profile/(?P<username>\w+)/$',views.profile, name='profile'),
	url(r'^register/$', views.register, name='register'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
	url(r'^add_match/$', views.add_match, name='add_match'),
	url(r'^(?P<game>\w+)/$', views.games, name='games'),
)