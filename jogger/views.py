from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from jogger.models import Choice, Poll, Node
from jogger.graph_preparation import route_processing, route_specification_data
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
    return render(request, 'jogger/route_index.html', context)

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