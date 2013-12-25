from django.http import Http404
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import simplejson
from polls.models import Choice, Poll, Node
import json

def ajax_test(request):
    if request.method == 'POST' and request.is_ajax():
        name = request.POST['name']
        city = request.POST['city']
        message = name + ' lives in ' + city
        return HttpResponse(json.dumps({'message': message}))
    return HttpResponse("You're looking at ajax_test")

def route_index(request):
    node_objs = Node.objects.all()
    context = {'nodes': node_objs }
    return render(request, 'polls/route_index.html', context)

def route_solutions(request):
    some_data_to_dump = {   'some_var_1': 'foo',
                            'some_var_2': 'bar',
                         }
    data = simplejson.dumps(some_data_to_dump)
    return HttpResponse(data, mimetype='application/json')


def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    context = {'latest_poll_list': latest_poll_list}
    return render(request, 'polls/index.html', context)

def detail(request, poll_id):
    try:
        poll = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404
    return render(request, 'polls/detail.html', {'poll': poll})

def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/results.html', {'poll': poll})

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
