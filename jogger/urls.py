from django.conf.urls import patterns, url

from jogger import views

urlpatterns = patterns('',
    url(r'^$', views.route_index, name='route'),
    url(r'^route_solutions/$', views.route_solutions, name='route_solutions'),
)