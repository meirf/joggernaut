from django.conf.urls import patterns, url

from jogger import views

urlpatterns = patterns('',
    url(r'^route/$', views.route_index, name='route'),

    url(r'^route_solutions/$', views.route_solutions, name='route_solutions'),

    url(r'^ajax/$', views.ajax_test, name="ajax"),

)