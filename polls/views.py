from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from polls.models import Choice, Poll, Node
from polls.graph_preparation import route_processing, route_specification_data
import json

def ajax_test(request):
    if request.method == 'GET' and request.is_ajax():
        name = request.GET['name']
        city = request.GET['city']
        message = name + ' lives in ' + city
        return HttpResponse(json.dumps({'message': message}))
    return HttpResponse("You're looking at ajax_test")

def route_index(request):
    node_objs = Node.objects.all()
    context = { 'nodes': node_objs }
    return render(request, 'polls/route_index.html', context)

def route_solutions(request):
    if request.method == 'GET' and request.is_ajax():
        a = request.GET['source_node_id']
        b = request.GET['dist_min']
        c = request.GET['dist_max']
        d = request.GET['elev_min_a']
        e = request.GET['elev_min_b']
        f = request.GET['elev_max_a']
        g = request.GET['elev_max_b']
        input_specs = route_specification_data.RouteSpecs(int(a), int(b), int(c), int(d), int(e), int(f), int(g))
        route_response = route_processing.main_route_calculator(input_specs)
        return HttpResponse(json.dumps(route_response), content_type="application/json")
    return HttpResponse("You're looking at route_solutions non ajax-ly")

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
