import datetime
import pytz
from django.contrib.auth.models import User
from django.db import models
from home.validators import validate_file_extension


class SignUp(models.Model):
    active = models.BooleanField(default=True)


class Magazine(models.Model):
    name = models.CharField(max_length=60)
    version = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    image = models.FileField(default='')
    components = models.CharField(max_length=100, default='')
    other_img = models.FileField(null=True, default='')
    description = models.CharField(default='', max_length=200)
    license = models.BooleanField(default=True)


class PasswordRecovery(models.Model):
    """
    Основная модель для восстановления пароля

    :param active:  параметр активности
    :param token_1: первый токен
    :param token_2: второй токен
    :param email: email
    :param code: код
    :param expires: время окончания работы токенов
    :param confirm_token_1: первый токен
    :param confirm_token_2: второй токен
    """
    active = models.BooleanField(default=True)
    token_1 = models.CharField(default="", max_length=65)
    token_2 = models.CharField(default="", max_length=65)
    email = models.EmailField()
    tries_left = models.IntegerField(default=3)
    expires = models.DateTimeField(default=datetime.datetime.now(
        pytz.utc) + datetime.timedelta(hours=24))
    confirm_token_1 = models.CharField(default="", max_length=65)
    confirm_token_2 = models.CharField(default="", max_length=65)
    code = models.IntegerField(default=100000)


class Home(models.Model):
    """
    Основная модель для хранения дома

    :param theme: тема
    :param name: название
    :param city: город
    :param user: ForeignKey к модели :class:`django.contrib.auth.models.User`
    """
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, blank=True, null=False)
    name = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=168, default="")


class Room(models.Model):
    """
    Основная модель для хранения квартир

    :param flat: квартира
    :param name: название
    """
    house = models.ForeignKey(
        to=Home, on_delete=models.CASCADE, blank=True, null=False)
    name = models.CharField(max_length=100, default="Room")


class CodeCondition(models.Model):
    """
    Код для перезаписи значений сенсора состояния воздуха

    :param room: комната
    :param code: код для перезаписи значений датчика
    """
    room = models.ForeignKey(
        to=Room, on_delete=models.CASCADE, blank=True, null=False)
    code = models.CharField(default="", max_length=65)


class Condition(models.Model):
    """
    Основная модель для сенсора состояния воздуха

    :param code: код доступа к данному датчику
    :param room: комната нахождения датчика
    :param temperature: температура
    :param pressure: давление
    :param co2: количество co2
    :param humidity: влажность воздуха
    """
    name = models.CharField(max_length=100, default="Датчики")
    code = models.ForeignKey(
        to=CodeCondition, on_delete=models.CASCADE, blank=True, null=False)
    room = models.ForeignKey(
        to=Room, on_delete=models.CASCADE, blank=True, null=False)
    temperature = models.IntegerField()
    pressure = models.IntegerField()
    co2 = models.IntegerField()
    humidity = models.IntegerField()


class CodeDoor(models.Model):
    """
    Код для перезаписи значений сенсора двери

    :param room: комната
    :param code: код для перезаписи значений датчика
    """
    room = models.ForeignKey(
        to=Room, on_delete=models.CASCADE, blank=True, null=False)
    code = models.CharField(default="", max_length=65)


class Door(models.Model):
    """
    Основная модель для сенсора двери

    :param code: код доступа к данному датчику
    :param room: комната нахождения датчика
    :param opened: открыта ли дверь
    """
    name = models.CharField(max_length=100, default="Дверь")
    code = models.ForeignKey(
        to=CodeDoor, on_delete=models.CASCADE, blank=True, null=False)
    room = models.ForeignKey(
        to=Room, on_delete=models.CASCADE, blank=True, null=False)
    opened = models.BooleanField(default=False)  # 0 - closed; 1 - opened


class CodeWindow(models.Model):
    """
    Код для перезаписи значений сенсора окна

    :param room: комната
    :param code: код для перезаписи значений датчика
    """
    room = models.ForeignKey(
        to=Room, on_delete=models.CASCADE, blank=True, null=False)
    code = models.CharField(default="", max_length=65)


class Window(models.Model):
    """
    Основная модель для сенсора окна

    :param code: код доступа к данному датчику
    :param room: комната нахождения датчика
    :param opened: открыта ли дверь
    """
    name = models.CharField(max_length=100, default="Окно")
    code = models.ForeignKey(
        to=CodeDoor, on_delete=models.CASCADE, blank=True, null=False)
    room = models.ForeignKey(
        to=Room, on_delete=models.CASCADE, blank=True, null=False)
    opened = models.BooleanField(default=False)  # 0 - closed; 1 - opened


class CodeLamp(models.Model):
    """
    Код для перезаписи значений сенсора лампы

    :param room: комната
    :param code: код для перезаписи значений датчика
    """
    room = models.ForeignKey(
        to=Room, on_delete=models.CASCADE, blank=True, null=False)
    code = models.CharField(default="", max_length=65)


class Lamp(models.Model):
    """
    Основная модель для сенсора лампы

    :param code: код доступа к данному датчику
    :param room: комната
    :param switched: включение лампочки
    :param color: цвет лампы
    """
    name = models.CharField(max_length=100, default="Лампа")
    code = models.ForeignKey(
        to=CodeLamp, on_delete=models.CASCADE, blank=True, null=False)
    room = models.ForeignKey(
        to=Room, on_delete=models.CASCADE, blank=True, null=False)
    switched = models.BooleanField(default=False)  # 0 - off; 1 - on;


class CodeSocket(models.Model):
    """
    Код для перезаписи значений сенсора лампы

    :param room: комната
    :param code: код для перезаписи значений датчика
    """
    room = models.ForeignKey(
        to=Room, on_delete=models.CASCADE, blank=True, null=False)
    code = models.CharField(default="", max_length=65)


class Socket(models.Model):
    """
    Основная модель для сенсора лампы

    :param code: код доступа к данному датчику
    :param room: комната
    :param switched: включение лампочки
    :param color: цвет лампы
    """
    name = models.CharField(max_length=100, default="Розетка")
    code = models.ForeignKey(
        to=CodeSocket, on_delete=models.CASCADE, blank=True, null=False)
    room = models.ForeignKey(
        to=Room, on_delete=models.CASCADE, blank=True, null=False)
    switched = models.BooleanField(default=False)  # 0 - off; 1 - on;


class Picture(models.Model):
    """
    Основная модель для загрузки фото

    :param file: изображение
    :param owner: пользователь загрузивший изображение
    """
    file = models.FileField(upload_to="pictures/",
                            validators=[validate_file_extension])
    owner = models.ForeignKey(
        to=User, on_delete=models.CASCADE, blank=True, null=False)


class LicenseCode(models.Model):
    """
    Модель лицензионного ключа

    :param code: активационный ключ лицензии
    :param type: какие устройства есть в лицензии 1 - есть лампа 2 - дисплей 3 - дверь 4 - датчик воздуха
    """
    code = models.CharField(default="", max_length=20)
    type = models.CharField(default="1", max_length=4)


class Personalization(models.Model):
    """
    Основная модель для хранения персонализации

    :param theme: тема
    :param user: ForeignKey к модели :class:`django.contrib.auth.models.User`
    :param room: комната, которая открывается в панели
    """
    home = models.ForeignKey(to=Home, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    theme = models.IntegerField(default=1)  # 0 - light; 1 - dark; 2-auto
