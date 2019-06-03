"""
Получение данных с датчиков
"""

import datetime
from django.shortcuts import render
import random
from hashlib import sha256
from home.models import Condition, Door, Relay, CodeCondition, CodeDoor, CodeRelay
from home.views import handler404


def condition(request):
    """
    Получение данных от термодатчика
    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: при успешной записи данных новый токен
    :rtype: :class:`django.http.HttpResponse`
    """
    temperature = int(request.GET.get("temperature", ""))
    pressure = int(request.GET.get("pressure", ""))
    co2 = int(request.GET.get("co2", ""))
    humidity = int(request.GET.get("humidity", ""))
    code = request.GET.get("code", "")  # for identification Arduino
    if 410 >= co2 > 4900:
        co2 = 0
    try:
        code_object = CodeCondition.objects.get(code=code)
        condition_object = Condition.objects.filter(code=code_object)
        if co2 != 0:
            if len(condition_object) == 0:
                condition_object = Condition(room=code_object.room,
                                             code=code_object,
                                             temperature=temperature,
                                             pressure=pressure,
                                             co2=co2,
                                             humidity=humidity)
            else:
                condition_object = condition_object[0]
                condition_object.temperature = temperature
                condition_object.pressure = pressure
                condition_object.co2 = co2
                condition_object.humidity = humidity
        else:
            if len(condition_object) == 0:
                condition_object = Condition(room=code_object.room,
                                             code=code_object,
                                             temperature=temperature,
                                             co2=co2,
                                             pressure=pressure,
                                             humidity=humidity)
            else:
                condition_object = condition_object[0]
                condition_object.temperature = temperature
                condition_object.pressure = pressure
                condition_object.humidity = humidity
        condition_object.save()
        context = {'code': 'Success'}
        return render(request, "dispatcher/success.html", context)
    except CodeCondition.DoesNotExist:
        return handler404(request)


def door(request):
    """
    Получение данных от датчика дверей
    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: при успешной записи данных новый токен
    :rtype: :class:`django.http.HttpResponse`
    """
    opened = int(request.GET.get("opened", ""))
    code = request.GET.get("code", "")
    try:
        code_object = CodeDoor.objects.get(code=code)
        door_object = Door.objects.filter(code=code_object)
        if len(door_object) == 0:
            door_object = Door(opened=opened,
                               code=code_object,
                               room=code_object.room)
        else:
            door_object = door_object[0]
            door_object.opened = opened
        door_object.save()
        context = {'code': "Success"}
        code_object.save()
        return render(request, "dispatcher/success.html", context)
    except CodeDoor.DoesNotExist:
        return render(request, "dispatcher/error404.html", )


def relay(request):
    """
    Получение данных от датчика реле
    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: при успешной записи данных новый токен
    :rtype: :class:`django.http.HttpResponse`
    """
    try:
        code = request.GET.get("code", "")
        code_object = CodeRelay.objects.get(code=code)
        relay_object = Relay.objects.filter(code=code_object)
        if len(relay_object) == 0:
            relay_object = Relay(room=code_object.room, switched=True, code=code_object)
            relay_object.save()
            context = {'code': 'no data'}
        elif relay_object[0].switched:
            context = {'code': 4}  # True
        else:
            context = {'code': 7}  # False
        return render(request, "dispatcher/success_for_receiver.html", context)
    except CodeRelay.DoesNotExist:
        return render(request, "dispatcher/error404.html", )
