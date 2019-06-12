import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from home.models import Room, Home, Personalization, Lamp
from home.views import check_key, generate_codes


@login_required(login_url="/login/")
def delete_room(request, room):
    """
    Страница удаления комнаты

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :param home: идентификатор дома
    :param room: идентификатор комнаты
    :return: шаблон удаления комнаты
    """
    try:
        room_obj = Room.objects.get(id=room)
        if request.user == room_obj.house.user:
            room_obj.delete()
            return HttpResponse('')
        else:
            return HttpResponse(status=403)
    except Home.DoesNotExist or Room.DoesNotExist:
        return HttpResponse('', status=404)


@login_required(login_url="/login/")
def delete_home(request, home):
    """
    Страница удаления дома

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :param home: идентификатор дома
    :return: шаблон удаления дома
    """
    try:
        house = Home.objects.get(id=home)
        rooms = Room.objects.filter(house=house)
        if request.user == house.user:
            house.delete()
            for room in rooms:
                room.delete()
        return HttpResponse('')
    except Room.DoesNotExist or Home.DoesNotExist:
        return HttpResponse(status=404)


@login_required(login_url="/login/")
def edit_home(request, home):
    """
    Страница редактирования дома

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :param home: идентификатор дома
    :return: шаблон редактирования дома
    """
    try:
        home_object = Home.objects.get(id=home)
        if request.user == home_object.user and request.is_ajax() and request.method == "POST":
            data = json.loads(request.body)
            try:
                home_object.name = data['name']
                home_object.city = data['city']
                home_object.save()
                return HttpResponse("ok")
            except KeyError:
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=403)
    except Room.DoesNotExist:
        return HttpResponse(status=404)


@login_required(login_url="/login/")
def edit_room(request, room):
    """
    Страница редактирования комнаты

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :param home: идентификатор дома
    :param room: идентификатор комнаты
    :return: шаблон удаления комнаты
    """
    try:
        room_object = Room.objects.get(id=room)
        if request.user == room_object.house.user and request.is_ajax() and request.method == "POST":
            data = json.loads(request.body)
            try:
                room_object.name = data['name']
                room_object.save()
                return HttpResponse("ok")
            except KeyError:
                pass
        else:
            return HttpResponse(status=403)
    except Room.DoesNotExist:
        return HttpResponse(status=404)


@login_required(login_url="/login/")
def add_room(request, home):
    try:
        home_object = Room.objects.get(id=home)
        if request.user == home_object.user and request.is_ajax() and request.method == "POST":
            data = json.loads(request.body)
            if check_key(data["key"]):
                try:
                    room = Room(name=data["name"], house=home_object)
                    room.save()
                    generate_codes(room=room, key=data["key"])
                    return HttpResponse("ok")
                except KeyError:
                    return HttpResponse('bad_request')
            else:
                return HttpResponse("wrong_key")
        else:
            return HttpResponse(status=403)
    except Home.DoesNotExist:
        return HttpResponse(status=404)


@login_required(login_url="/login/")
def change_house(request, house_id):
    """
    Страница редактирования домов

    :param house_id: идентификатор дома, на который требуется переключиться
    :type house_id: :class:`int`
    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: перенаправление на панель
    """
    try:
        home = Home.objects.get(id=house_id)
        if home.user == request.user:
            try:
                personalization = Personalization.objects.get(user=request.user)
                personalization.home = home
                personalization.save()
                return HttpResponse('')
            except Personalization.DoesNotExist:
                return HttpResponse(status=404)
        else:
            return HttpResponse(status=403)
    except Home.DoesNotExist:
        return HttpResponse(status=404)


@login_required(login_url='/login/')
def lamp_room(request, lamp, on):
    """
    Страница включения всех реле в комнате

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: панель с включенными реле
    """
    try:
        lamp = Lamp.objects.get(id=lamp)
        if request.user == lamp.room.house.user:
            lamp.switched = True if on == "on" else False
            lamp.save()
        return HttpResponse('')
    except Lamp.DoesNotExist:
        return HttpResponse('')


@login_required(login_url='/login/')
def lamp_house(request, on):
    """
    Страница включения всех реле в доме

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: панель с включенными реле
    """
    current = Personalization.objects.get(user=request.user).home
    for room in Room.objects.filter(house=current):
        lamps = Lamp.objects.filter(room=room)
        for lamp in lamps:
            lamp.switched = True if on == "on" else False
            lamp.save()
    return HttpResponse('')
