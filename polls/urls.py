from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns('',
    url(r'^route/$', views.route_index, name='route'),

    url(r'^route_solutions/$', views.route_solutions, name='route_solutions'),

    url(r'^ajax/$', views.ajax_test, name="ajax"),

    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    url(r'^(?P<poll_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<poll_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<poll_id>\d+)/vote/$', views.vote, name='vote'),
)