__author__ = 'meirfischer'


def main_route_calculator(route_specs):
    response = {};
    try:
        check_inherent_specs(route_specs)
    except Exception, e:
        response["input_status"] = "InputError"
        response["response_data"] = e.message
        return response


def check_inherent_specs(route_specs):
    if route_specs.elev_min_b > route_specs.elev_max_b:
        raise Exception(str(route_specs.elev_min_b) + " is greater than " + str(route_specs.elev_max_b))
