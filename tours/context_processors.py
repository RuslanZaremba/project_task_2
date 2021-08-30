import tours.data as data


def departures_list(request):
    return {'title': data.title, 'departures_list': data.departures}
