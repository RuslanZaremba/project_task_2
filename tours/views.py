import tours.data as data

from django.http import HttpResponseNotFound, HttpResponseServerError, Http404
from django.shortcuts import render

from collections import OrderedDict
from random import randint


# def base_view(request):
#     context = {'title': data.title, 'departures': data.departures}
#     return render(request, 'tours/base.html', context=context)


def main_view(request):
    """Генерирую словарь с 6 рандомными турами"""
    num_random_positions = set()
    while len(num_random_positions) != 6:
        num_random_positions.add(randint(1, len(data.tours)))
    dict_from_6 = {}
    for i in num_random_positions:
        dict_from_6[i] = data.tours.get(i)

    context = {'title': data.title, 'subtitle': data.subtitle, 'description': data.description, 'tours': dict_from_6}
    return render(request, 'tours/index.html', context=context)


def departure_view(request, departure):
    """Создаем новый словарь с нужными данными по полю departure"""
    data_sort_by_departure = dict()
    new = OrderedDict(data.tours)
    for i in new:
        if new[i]['departure'] == departure:
            data_sort_by_departure[i] = new[i]
    """Достаем min и max значения цен"""
    list_prices = [v['price'] for k, v in data_sort_by_departure.items()]
    min_max_prices = {'min': min(list_prices), 'max': max(list_prices)}
    """Достаем min и max значения ночей"""
    list_nights = [v['nights'] for k, v in data_sort_by_departure.items()]
    min_max_nights = {'min': min(list_nights), 'max': max(list_nights)}
    """Получаем место отправления"""
    departure_with = data.departures[departure]

    context = {'departure_dict': data_sort_by_departure, 'prices': min_max_prices, 'min_max_nights': min_max_nights,
               'departure_with': departure_with}

    return render(request, 'tours/departure.html', context=context)


def tour_view(request, departure, id):
    try:
        tour = data.tours[id]
    except KeyError:
        raise Http404
    """Генерируем нужное колличество звезд"""
    stars = f"{int(tour.get('stars')) * '★'}"
    """Получаем место отправления"""
    departure_with = data.departures.get(tour.get('departure'))

    context = {'tour_id': id, 'tour': tour, 'stars': stars, 'departure_with': departure_with}

    return render(request, 'tours/tour.html', context=context)


def custom_handler404(request, exception):
    return HttpResponseNotFound('Ой, что то сломалось... Простите извините!')


def custom_handler500(request):
    # Call when raised some python exception
    return HttpResponseServerError('Ошибка сервера!')
