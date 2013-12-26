__author__ = 'meirfischer'

from polls.models import Node, Edge

#check elev ranges are allowable
def check_inherent_specs(route_specs):
    if route_specs.elev_min_b > route_specs.elev_max_b:
        raise Exception(str(route_specs.elev_min_b) + " is greater than " + str(route_specs.elev_max_b))


"""If there is no node in the pre-computed subsection
   with elevation in range X or there is no node in the
   pre-computed subsection with elevation in range Y,
   the user will be told what the upper limit elevation
   is or what the lower limit elevation is.
   """
def check_node_exists_in_elev_ranges(route_specs):
    if len(Node.objects.filter(elevation__gte=route_specs.elev_min_a).filter(elevation__lte=route_specs.elev_min_b))==0:
        raise Exception("No node exists with elevation in range: "+str(route_specs.elev_min_a)+" - "+str(route_specs.elev_min_b))
    if len(Node.objects.filter(elevation__gte=route_specs.elev_max_a).filter(elevation__lte=route_specs.elev_max_b))==0:
        raise Exception("No node exists with elevation in range: "+str(route_specs.elev_max_a)+" - "+str(route_specs.elev_max_b))


def main_route_calculator(route_specs):
    response = {};
    try:
        check_inherent_specs(route_specs)
        check_node_exists_in_elev_ranges(route_specs)
    except Exception, e:
        response["input_status"] = "BadInput"
        response["response_data"] = e.message
        return response




