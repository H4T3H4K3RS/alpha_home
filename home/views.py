"""
  View-функции
"""

import datetime
import random
from hashlib import sha256, md5
import pytz
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from home.forms import (
    LoginForm,
    UserRegistrationForm,
    AskForm,
    UploadImageForm,
    RecoverForm,
    RecoverCodeForm,
    NewPasswordForm,
    HomeForm,
    HiddenForm,
    EditRoomForm,
    LicenseForm,
    RoomForm,
    ProfileForm)
from home.apps.weather import get_weather
from home.apps.send_mail import send_mail
from home.apps.config.mail import email_contact
from home.models import (
    PasswordRecovery,
    Personalization,
    Home,
    Picture,
    Condition,
    Room,
    CodeDisplay,
    Relay,
    CodeRelay,
    Display,
    CodeDoor,
    Door,
    CodeCondition,
    LicenseCode,
    Magazine,
    SignUp,
)


def handle_theme(request, panel_type, context):
    template_name = None
    context["title"] = "Панель Управления"
    if panel_type is None:
        try:
            theme = Personalization.objects.get(user=request.user)
            context["auto"] = False
            if theme.theme == 1:
                context["panel_style_primary"] = "dark"
                context["panel_style_secondary"] = "light"
            elif theme.theme == 2:
                night_end = datetime.datetime(
                    year=1, month=1, day=1, hour=8, minute=0, second=0
                )
                night_start = datetime.datetime(
                    year=1, month=1, day=1, hour=20, minute=0, second=0
                )
                time = datetime.datetime.now(pytz.utc) + datetime.timedelta(hours=3)
                time = datetime.datetime(
                    year=1,
                    month=1,
                    day=1,
                    second=time.second,
                    hour=time.hour,
                    minute=time.minute,
                )
                if night_end < time < night_start:
                    context["panel_style_primary"] = "light"
                    context["panel_style_secondary"] = "dark"
                else:
                    context["panel_style_primary"] = "dark"
                    context["panel_style_secondary"] = "light"
                context["auto"] = True
            else:
                context["panel_style_primary"] = "light"
                context["panel_style_secondary"] = "dark"
        except Personalization.DoesNotExist:
            template_name = "choose_theme.html"
    elif panel_type == "dark":
        try:
            theme = Personalization.objects.get(user=request.user)
            theme.theme = 1
            theme.save()
        except Personalization.DoesNotExist:
            try:
                house = Home.objects.filter(user=request.user)[0]
                room = Room.objects.filter(house=house)[0]
                theme = Personalization()
                theme.theme = 1
                theme.room = room
                theme.user = request.user
                theme.save()
            except IndexError:
                return redirect("/edit/")
        return redirect("/panel/")
    elif panel_type == "auto":
        try:
            theme = Personalization.objects.get(user=request.user)
            theme.theme = 2
            theme.save()
        except Personalization.DoesNotExist:
            try:
                house = Home.objects.filter(user=request.user)[0]
                room = Room.objects.filter(house=house)[0]
                theme = Personalization()
                theme.theme = 2
                theme.room = room
                theme.user = request.user
                theme.save()
            except IndexError:
                messages.error(request, "Не добавлена комната")
                return redirect("/edit/")
        return redirect("/panel/")
    elif panel_type == "light":
        try:
            theme = Personalization.objects.get(user=request.user)
            theme.theme = 0
            theme.save()
        except Personalization.DoesNotExist:
            try:
                house = Home.objects.filter(user=request.user)[0]
                room = Room.objects.filter(house=house)[0]
                theme = Personalization()
                theme.theme = 0
                theme.room = room
                theme.user = request.user
                theme.save()
            except IndexError:
                return redirect("/edit/")
        return redirect("/panel/")
    else:
        return handler404(request)
    return template_name, context


def add_data(request, context=None, test=False):
    """
    Добавление данных датчиков на панель

    :param context: контекст, который нужно дополнить
    :type context: :class:`dict`
    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера с HTML-кодом внутри
    :rtype: :class:`dict`
    """
    if context is None:
        context = {}
    context["api"] = {}
    indicators = get_weather()
    if indicators != {}:
        context["api"]["temperature"] = indicators[0]
        context["api"]["condition"] = indicators[1]
        context["api"]["wind_speed"] = indicators[2]
        context["api"]["wind_dir"] = indicators[3]
        context["api"]["humidity"] = indicators[4]
        context["api"]["pressure"] = indicators[6]
        context["api"]["precipitation"] = indicators[7]
        context["api"]["precipitation_mm"] = indicators[8]
        context["api"]["feels_like"] = indicators[9]
    else:
        context["api"]["temperature"] = "NaN"
        context["api"]["condition"] = "NaN"
        context["api"]["wind_speed"] = "NaN"
        context["api"]["wind_dir"] = "NaN"
        context["api"]["humidity"] = "NaN"
        context["api"]["pressure"] = "NaN"
        context["api"]["precipitation"] = "NaN"
        context["api"]["precipitation_mm"] = "NaN"
        context["api"]["feels_like"] = "NaN"
    now = datetime.datetime.now()
    context["date"] = now.date
    if test:
        context["condition"] = {}
        context["condition"]["temperature"] = 22  # Celsius
        context["condition"]["co2"] = 1000  # ppm
        context["condition"]["humidity"] = 20  # % percents
        context["condition"]["pressure"] = 750  # mm of Hg
        context["lamp"] = {}
        context["lamp"]["switched"] = 0  # 1 - on; 0 - off
        context["display"] = {}
        context["display"]["number"] = 0  # integer
        context["display"]["time"] = 1  # minutes
        context["door"] = {}
        context["door"]["opened"] = 0  # 1 - opened; 0 - closed
    else:
        try:
            default = Personalization.objects.get(user=request.user)
            room = default.room
            context["rooms"] = {}
            context["rooms"]["current"] = room
            if room is None:
                return None
            context["rooms"]["other"] = []
            rooms_other = Room.objects.filter(house=room.house)
            for room_obj in rooms_other:
                if room_obj != room:
                    context["rooms"]["other"].append(room_obj)
            context["houses"] = {}
            context["houses"]["current"] = room.house
            context["houses"]["other"] = []
            homes_other = Home.objects.filter(user=request.user)
            for home in homes_other:
                if home != room.house:
                    context["houses"]["other"].append(home)
            try:
                relay = Relay.objects.get(room=room)
                context["lamp"] = {}
                context["lamp"]["switched"] = relay.switched  # 1 - on; 0 - off
            except Relay.DoesNotExist:
                context["lamp"] = 0
            try:
                display = Display.objects.get(room=room)
                context["display"] = {}
                context["display"]["number"] = display.number  # integer
                context["display"]["time"] = display.expires  # minutes
            except Display.DoesNotExist:
                context["display"] = 0
            try:
                condition = Condition.objects.get(room=room)
                context["condition"] = {}
                # Celsius
                context["condition"]["temperature"] = int(condition.temperature)
                context["condition"]["co2"] = int(condition.co2)  # ppm
                # % percents
                context["condition"]["humidity"] = int(condition.humidity)
                context["condition"]["pressure"] = int(condition.pressure)  # mm of Hg
            except Condition.DoesNotExist:
                context["condition"] = 0
            try:
                door = Door.objects.get(room=room)
                context["door"] = {}
                # 1 - opened; 0 - closed
                context["door"]["opened"] = door.opened
            except Door.DoesNotExist:
                context["door"] = 0
        except Personalization.DoesNotExist:
            pass
    return context


def get_base_context():
    """
    Функция заполняющая словарь context базовым контекстом

    :return: словарь с предустановленными значениями
    :rtype: :class:`dict`
    """
    context = {"phone": "+7(964)578-53-44", "email": 'home@umtechn.ru'}
    return context


def new_license(cmd=""):
    """

    :param cmd: строка содержащие типы датчиков для лицензии
    :return:
    """
    now = datetime.datetime.now()
    secret = "bdhgbaghjdhj{}wbedjhqb!@jhwbjhJSHBA{}!&^&@**@(@!(*HJGHSFGHVHG!VWHGV~!G@WV{}SHGVAHGVSHGVWSHGVHGV{}"
    first_code = str(
        random.randint(1001001010190219019209, 219820183013849208042432676867687)
    ) + secret.format(str(now.hour), str(now.day), str(now.year), str(now.month))
    code = (
            str(random.randint(10000, 22677))
            + md5(
        str(
            sha256("jehfjehfjhe".encode()).hexdigest()
            + first_code
            + md5("123123".encode()).hexdigest()
        ).encode()
    ).hexdigest()[5:20]
    )
    activation = LicenseCode(type=cmd, code=code)
    activation.save()
    return code


def check_key(key):
    """
    Проверка ключа активации
    :param key: ключ активации, который нужно проверить
    :type key: :class:`str`
    :return: Правильный ли ключ
    :rtype: :class:`bool`
    """
    try:
        LicenseCode.objects.get(code=key)
        return True
    except LicenseCode.DoesNotExist:
        return False


def generate_codes(room, key):
    """
    Создание кодов доступа для датчиков, подключённых

    :param room: комната, в которой будут находится датчики
    :param key: ключ активации
    :return:
    """
    activation = LicenseCode.objects.get(code=key)
    if "1" in activation.code:
        model = CodeRelay(room=room, code=key)
        model.save()
    if "2" in activation.code:
        model = CodeDisplay(room=room, code=key)
        model.save()
    if "3" in activation.code:
        model = CodeDoor(room=room, code=key)
        model.save()
    if "4" in activation.code:
        model = CodeCondition(room=room, code=key)
        model.save()
    activation.delete()
    return


def agreement(request):
    """
    Страница соглашения

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера с HTML-кодом внутри
    :rtype: :class:`django.http.HttpResponse`
    """
    context = get_base_context()
    return render(request, "agreement.html", context)


def success(request, title="", text="", template_name="success.html"):
    """
    Функция перенаправляющая на главную страницу при возниковении
    ошибки или создание многновенного сообщения

    :param template_name: путь к шаблону
    :param text: текст, который будет отображаться на странице
    :param title: заголовок страницы
    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера с HTML-кодом внутри
    :rtype: :class:`django.http.HttpResponse`
    """
    context = get_base_context()
    context["title"] = title
    context["text"] = text
    return render(request, template_name, context)


def handler404(request):
    """
    Страница ошибки 404

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера с HTML-кодом внутри
    :rtype: :class:`django.http.HttpResponse`
    """
    return render(request, "404.html", status=404)


def handler403(request):
    """
    Страница ошибки 403

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера с HTML-кодом внутри
    :rtype: :class:`django.http.HttpResponse`
    """
    return render(request, "403.html", status=403)


def handler500(request):
    """
    Страница ошибки 505

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера с HTML-кодом внутри
    :rtype: :class:`django.http.HttpResponse`
    """
    return render(request, "505.html", status=500)


def index_page(request):
    """
    Главная страница

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: объект ответа сервера с HTML-кодом внутри
    :rtype: :class:`django.http.HttpResponse`
    """
    context = get_base_context()
    context["title"] = "Главная страница - Alpha Home"
    if request.user.is_authenticated:
        context['form'] = AskForm(initial={
            'Name': str(request.user.first_name) + str(request.user.last_name),
            'Email': request.user.email
        })
    else:
        context['form'] = AskForm()
    return render(request, "index.html", context)


def authorize_page(request):
    """
    Страница авторизации

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: Перенаправление на главную страницу

    """

    context = get_base_context()
    context["title"] = "Войти"
    if request.method == "POST":
        if not request.POST.get("remember_me", None):
            request.session.set_expiry(0)
        form = LoginForm(request.POST)
        if form.is_valid():
            context["form"] = form
            username = form.data["login"]
            password = form.data["password"]
            try:
                username = User.objects.get(username=username).username
            except User.DoesNotExist:
                try:
                    username = User.objects.get(email=username).username
                except User.DoesNotExist:
                    messages.error(request, "Логин/Email неверный")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/panel/")
            else:
                try:
                    User.objects.get(username=username)
                    messages.error(request, "Неверный пароль")
                except User.DoesNotExist:
                    messages.error(request, "Логин/Email неверный")
        else:
            messages.error(request, "Неправильный формат данных.")
    else:
        context["form"] = LoginForm()
    return render(request, "authorize.html", context)


def register_page(request):
    """
    Страница регистрации

    :param request: Объект с деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: Перенаправление на главную страницу
    """
    try:
        signup = SignUp.objects.get(id=1)
        if not signup.active:
            messages.error(request, "Регистрация закрыта.")
            return redirect("/login/")
    except SignUp.DoesNotExist:
        signup = SignUp()
        signup.save()
    context = get_base_context()
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            users_email = User.objects.filter(email=user_form.data["email"])
            if users_email:
                messages.error(request, "Пользователь с таким email уже существует.")
                context["form"] = UserRegistrationForm()
                return render(request, "register.html", context)
            else:
                new_user = user_form.save(commit=True)
                new_user.set_password(user_form.cleaned_data["password"])
                new_user.save()
                username = str(user_form.data["username"])
                password = str(user_form.data["password"])
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                return redirect("/panel/")
        else:
            users = User.objects.filter(username=user_form.data["username"])

            if users is not []:
                messages.error(request, "Пользователь с таким именем уже существует.")
            elif user_form.data["password"] != user_form.data["password2"]:
                messages.error(request, "Пароли не совпадают.")
            else:
                messages.error(request, "Неверный email.")
            context["form"] = UserRegistrationForm()

    else:
        context["form"] = UserRegistrationForm()
    return render(request, "register.html", context)


def logout_page(request):
    """
    Выход из профиля

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: перенаправление на главную страницу

    """

    logout(request)
    return redirect("/")


def ask(request):
    """
    Стрвница для отправки вопросов

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: перенаправление на главную страницу

    """

    context = get_base_context()
    context["title"] = "Обращение в тех.поддрежку"
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            name = form.data["Name"]
            email = form.data["Email"]
            question = form.data["Question"]
            author = request.user
            send_mail(name=name, email=email, author=str(author), question=question)
            return success(request, "Заявка", "Заявка получена.")
        else:
            messages.error(request, "Неправильный формат данных")
            context["form"] = AskForm()
    else:
        context["form"] = AskForm()
    return render(request, "ask_form.html", context)


def set_password(request, confirm_token_1=None, confirm_token_2=None):
    """
    Страница восстановления пароля

    :param confirm_token_1: первый токен для перехода на страницу установки нового пароля
    :param confirm_token_2: второй токен для перехода на страницу установки нового пароля
    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: перенаправление на следующую страницу
    :return: перенаправление на эту же страницу при ошибке
    """

    context = get_base_context()
    if confirm_token_1 is None or confirm_token_2 is None:
        return redirect("/")
    elif (confirm_token_1 is not None) and (confirm_token_2 is not None):
        if request.method == "POST":
            form = NewPasswordForm(request.POST)
            if form.is_valid():
                try:
                    recovery = PasswordRecovery.objects.get(
                        confirm_token_1=confirm_token_1, confirm_token_2=confirm_token_2
                    )
                    context["token_1"] = confirm_token_1
                    context["token_2"] = confirm_token_2
                    if datetime.datetime.now(pytz.utc) > recovery.expires:
                        context["form"] = NewPasswordForm()
                        messages.error(request, "Токены просрочены.")
                        recovery.delete()
                        return render(
                            request, "recover_password/set_password.html", context
                        )
                    else:
                        if form.data["password"] != form.data["password2"]:
                            context["form"] = NewPasswordForm()
                            messages.error(request, "Пароли не совпадают.")
                            recovery.delete()
                            return render(
                                request, "recover_password/set_password.html", context
                            )
                        else:
                            try:
                                user = User.objects.get(email=recovery.email)
                                user.set_password(form.cleaned_data["password"])
                                user.save()
                                username = user.username
                                password = form.cleaned_data["password"]
                                user = authenticate(
                                    request, username=username, password=password
                                )
                                login(request, user)
                                recovery.delete()
                                return redirect("/")
                            except User.DoesNotExist:
                                return redirect("/")
                except PasswordRecovery.DoesNotExist:
                    context["form"] = NewPasswordForm()
                    messages.error(request, "Неправильные токены.")
                    return render(
                        request, "recover_password/set_password.html", context
                    )
            else:
                context["form"] = NewPasswordForm()
                messages.error(request, "Неправильные данные")
                return render(request, "recover_password/set_password.html", context)
        else:
            context["token_1"] = confirm_token_1
            context["token_2"] = confirm_token_2
            context["form"] = NewPasswordForm()
            return render(request, "recover_password/set_password.html", context)


def control_panel(requests):
    return render(requests, 'control_panel.html', )


def recover(request, token_1=None, token_2=None):
    """
    Функция, создающая хэш ссылки, для восстановления пароля

    :param token_1: первый токен для доступа к странице ввода 6-значного кода
    :param token_2: второй токен для доступа к странице ввода 6-значного кода
    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: перенаправление на последущую страницу при успешном восстановлении
    :return: перенаправление на эту же страницу при ошибке
    """
    context = get_base_context()
    if str(request.user) == "AnonymousUser":
        if (token_1 is None) or (token_2 is None):
            if request.method == "POST":
                form = RecoverForm(request.POST)
                if form.is_valid():
                    try:
                        User.objects.get(email=form.data["email"])
                        token = PasswordRecovery()
                        token.email = form.data["email"]
                        code = random.randint(100000, 999999)
                        token_1 = sha256(
                            (
                                "23r341t11{}q34t4qgfreg{}qergqe".format(
                                    form.data["email"], code
                                )
                            ).encode()
                        ).hexdigest()
                        token_2 = sha256(
                            (
                                "23fq3fq3{}4ssfe3sdv23rf{}hwasbefjbgwefj".format(
                                    form.data["email"], code
                                )
                            ).encode()
                        ).hexdigest()
                        confirm_token_1 = sha256(
                            (
                                "23rewr4tfwef341t11{}q2d3423242b3b434t4qgfreg{}qerb43gqe".format(
                                    form.data["email"], code
                                )
                            ).encode()
                        ).hexdigest()
                        confirm_token_2 = sha256(
                            (
                                "wef23r24fq3fq3{}d3244ssf32d3e3sdv23rf{}hwasbefb2b34jbgwefj".format(
                                    form.data["email"], code
                                )
                            ).encode()
                        ).hexdigest()
                        token.token_1 = token_1
                        token.token_2 = token_2
                        token.confirm_token_1 = confirm_token_1
                        token.confirm_token_2 = confirm_token_2
                        token.code = code
                        token.save()
                        send_mail(
                            confirm=True,
                            email=form.data["email"],
                            code=code,
                            recover_link="https://home.umtechn.ru/recover/confirm/{}/{}".format(
                                confirm_token_1, confirm_token_2
                            ),
                            unrecover_link="https://home.umtechn.ru/unrecover/{}/{}".format(
                                confirm_token_1, confirm_token_2
                            ),
                        )
                        return redirect("/recover/{}/{}".format(token_1, token_2))
                    except User.DoesNotExist:
                        context["form"] = RecoverForm()
                        messages.error(
                            request, "Пользователя с таким Email не существует."
                        )
                        return render(
                            request, "recover_password/email_input.html", context
                        )
                else:
                    context["form"] = RecoverForm()
                    messages.error(request, "Неверные данные.")
                    return render(request, "recover_password/email_input.html", context)
            else:
                context["form"] = RecoverForm()
                return render(request, "recover_password/email_input.html", context)
        elif (token_1 is not None) and (token_2 is not None):
            if request.method == "POST":
                form = RecoverCodeForm(request.POST)
                if form.is_valid():
                    try:
                        recovery = PasswordRecovery.objects.get(
                            token_1=token_1, token_2=token_2
                        )
                        context["token_1"] = token_1
                        context["token_2"] = token_2
                        if datetime.datetime.now(pytz.utc) > recovery.expires:
                            context["form"] = RecoverCodeForm()
                            messages.error(request, "Код и токены просрочены.")
                            return render(
                                request, "recover_password/code_input.html", context
                            )
                        elif recovery.tries_left == 0:
                            context["form"] = RecoverCodeForm()
                            messages.error(
                                request,
                                'Количество попыток исчерпано. Ввести Email повторно.',
                            )
                            recovery.delete()
                            return render(
                                request, "recover_password/code_input.html", context
                            )
                        elif str(recovery.code) == str(form.data["code"]):
                            return redirect(
                                "/recover/confirm/{}/{}/".format(
                                    recovery.confirm_token_1, recovery.confirm_token_2
                                )
                            )
                        else:
                            recovery.tries_left -= 1
                            recovery.save()
                            context["form"] = RecoverCodeForm()
                            if recovery.tries_left != 0:
                                messages.error(
                                    request,
                                    "Неверный код. Отсалось попыток: "
                                    + str(recovery.tries_left)
                                    + ".",
                                )
                            else:
                                messages.error(
                                    request,
                                    'Количество попыток исчерпано. Введите Email повторно.',
                                )
                                return redirect('/recover/')
                            return render(
                                request, "recover_password/code_input.html", context
                            )
                    except PasswordRecovery.DoesNotExist:
                        context["form"] = RecoverCodeForm()
                        messages.error(request, "Неправильные токены.")
                        return redirect('/recover/')
                else:
                    context["token_1"] = token_1
                    context["token_2"] = token_2
                    messages.error(
                        request, "Неверный формат кода. Введите 6-значный код."
                    )
                    context["form"] = RecoverCodeForm()
                    return render(request, "recover_password/code_input.html", context)
            else:
                context["token_1"] = token_1
                context["token_2"] = token_2
                context["form"] = RecoverCodeForm()
                return render(request, "recover_password/code_input.html", context)
        else:
            return redirect("/")
    else:
        return success(request, "Ошибка.", "Вы уже вошли в систему.")


def undo_recover(request, confirm_token_1=None, confirm_token_2=None):
    """
    Функция отмены подтверждения пароля

    :param confirm_token_1: первый токен для отмены восстановления пароля
    :param confirm_token_2: второй токен для отмены восстановления пароля
    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: перенаправление на главную страницу
    """
    context = get_base_context()
    if (confirm_token_2 is None) or (confirm_token_1 is None):
        return success(request, "Ошибка", "Неправильные токены восстановления пароля.")
    else:
        try:
            recovery = PasswordRecovery.objects.get(
                confirm_token_1=confirm_token_1, confirm_token_2=confirm_token_2
            )
            recovery.delete()
            context["title"] = "Отмена восстановления пароля."
            context["text"] = "Заявка на отмену восстановления пароля успешно получена."
            return success(
                request,
                "Отмена восстановления пароля.",
                "Заявка на отмену восстановления пароля успешно получена.",
            )
        except PasswordRecovery.DoesNotExist:
            context["title"] = "Ошибка."
            context["text"] = "Неправильные токены восстановления пароля."
            return success(
                request, "Ошибка.", "Неправильные токены восстановления пароля."
            )


@login_required(login_url="/login/")
def panel_page(request, panel_type=None):
    """
    Страница панели

    :param panel_type: тема панели (авто, тёмная, светлая)
    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: перенаправление на панель
    """
    context = get_base_context()
    from django.http import HttpResponseRedirect

    if type(handle_theme(request, panel_type, context)) is not HttpResponseRedirect:
        template_name, context = handle_theme(request, panel_type, context)
    else:
        return handle_theme(request, panel_type, context)
    if template_name is None:
        template_name = "panel.html"
    context = add_data(request, context)
    if context is None:
        return redirect("/edit/")
    return render(request, template_name=template_name, context=context)


def instruction(request):
    """
    Страница инструкции

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: перенаправление на страницу инструкции
    """
    return render(request, template_name="help.html")


@login_required(login_url="/login/")
def upload_file(request):
    """
    Функция по загрузке файлов

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: перенаправление на панель
    :return: перенаправление на страницу загрузки
    """
    context = get_base_context()
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            file = Picture(file=request.FILES["file"], owner=request.user)
            file.save()
            return redirect("/panel/")
    else:
        context["form"] = UploadImageForm()
    return render(request, "upload.html", context)


@login_required(login_url="/login/")
def profile(request):
    """
    Страница профиля

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: перенаправление на страницу профиля
    :return: перенаправление на страницу 404 при ошибке
    """
    context = get_base_context()
    if request.method == "POST":
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            users_email = User.objects.filter(email=profile_form.data["email"])
            if users_email and profile_form.data['email'] != users_email[0].email:
                messages.error(request, "Пользователь с таким email уже существует.")
                context["form"] = ProfileForm(data={
                    'username': profile_form.data['username'],
                    'last_name': profile_form.data['last_name'],
                    'first_name': profile_form.data['first_name'],
                    'email': profile_form.data['email']
                })
                return render(request, "register.html", context)
            else:
                user = User.objects.get(username=request.user)
                user.username = username = str(profile_form.data["username"])
                user.last_name = str(profile_form.data["last_name"])
                user.first_name = str(profile_form.data["first_name"])
                user.email = str(profile_form.data["email"])
                print(profile_form.data['password'])
                if profile_form.data['password'] != "":
                    user.set_password(profile_form.cleaned_data["password"])
                user.save()
                if user is not None:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect("/profile/")
        else:
            users = User.objects.filter(username=profile_form.data["username"])
            if users and users[0].username != profile_form.data['username']:
                messages.error(request, "Пользователь с таким именем уже существует.")
            elif profile_form.data["password"] != profile_form.data["password2"]:
                messages.error(request, "Пароли не совпадают.")
            else:
                messages.error(request, "Неверный email.")
            context["form"] = ProfileForm(data={
                'username': profile_form.data['username'],
                'last_name': profile_form.data['last_name'],
                'first_name': profile_form.data['first_name'],
                'email': profile_form.data['email']
            })
        return redirect('/profile/')
    else:
        try:
            user = User.objects.get(username=request.user)
            data = {
                'username': user.username,
                'last_name': user.last_name,
                'first_name': user.first_name,
                'email': user.email
            }
            context['form'] = ProfileForm(data)
            return render(request, "profile.html", context)
        except User.DoesNotExist:
            return handler404(request)


@login_required(login_url="/login/")
def delete_room(request, home, room):
    """
    Страница удаления комнаты

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :param home: идентификатор дома
    :param room: идентификатор комнаты
    :return: шаблон удаления комнаты
    """
    try:
        house = Home.objects.get(id=home)
        context = get_base_context()
        context["title"] = "Удаление комнаты"
        room_obj = Room.objects.get(id=room)
        if request.user == house.user:
            if request.method == "POST":
                personalization = Personalization.objects.get(user=request.user)
                homes = Home.objects.filter(user=request.user)
                rooms = Room.objects.filter(house=house)
                if len(rooms) >= 2:
                    for i in rooms:
                        if i.id != room:
                            personalization.room = i
                            personalization.save()
                            break
                elif len(homes) >= 2:
                    for i in homes:
                        rooms = Room.objects.filter(house=i)
                        for j in rooms:
                            if j.id != room:
                                personalization.room = j
                                personalization.save()
                                break
                room_obj.delete()
                return redirect("/edit/" + str(home))
            else:
                context["home"] = house
                context["room"] = room_obj
                context["form"] = HiddenForm()
                return render(request, "houses/room/delete.html", context)
        else:
            return handler403(request)
    except Home.DoesNotExist or Room.DoesNotExist:
        return handler404(request)


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
        context = get_base_context()
        context["title"] = "Удаление опроса"
        rooms = Room.objects.filter(house=house)
        if request.user == house.user:
            if request.method == "POST":
                house.delete()
                for room in rooms:
                    room.delete()
                return redirect("/edit/")
            else:
                context["home"] = house
                context["form"] = HiddenForm()
                return render(request, "houses/delete.html", context)
        else:
            return handler403(request)
    except Room.DoesNotExist or Home.DoesNotExist:
        return handler404(request)


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
        house = Home.objects.get(id=home)
        rooms = Room.objects.filter(house=house)
        if request.user == house.user:
            context = get_base_context()
            context["title"] = "Редактирование дома"
            context["home"] = house
            context["rooms"] = rooms
            if request.method == "POST":
                form = HomeForm(request.POST)
                if form.is_valid():
                    house.name = form.data["name"]
                    house.city = form.data["city"]
                    house.save()
                    return redirect("/edit/")
                else:
                    context["form_room"] = RoomForm()
                    context["form"] = HomeForm()
            else:
                context["form_room"] = RoomForm()
                context["form"] = HomeForm()
            return render(request, "houses/edit.html", context)
        else:
            return handler403(request)
    except Home.DoesNotExist:
        return handler404(request)


@login_required(login_url="/login/")
def edit_room(request, home, room):
    """
    Страница редактирования комнаты

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :param home: идентификатор дома
    :param room: идентификатор комнаты
    :return: шаблон удаления комнаты
    """
    try:
        house = Home.objects.get(id=home)
        if request.user == house.user:
            room_object = Room.objects.get(id=room)
            context = get_base_context()
            context["title"] = "Редактирование варианта опроса"
            context["home"] = house
            context["room"] = room_object
            if request.method == "POST":
                form = EditRoomForm(request.POST)
                if form.is_valid():
                    room_object.name = form.data["name"]
                    room_object.save()
                    return redirect("/edit/" + str(house.id))
            else:
                context["form"] = EditRoomForm()
                return render(request, "houses/room/edit.html", context)
        else:
            return handler403(request)
    except Home.DoesNotExist:
        return handler404(request)


@login_required(login_url="/login/")
def edit_houses(request):
    """
    Страница редактирования домов

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: шаблон редактирования домов
    """
    try:
        context = get_base_context()
        context["title"] = "Редактирование Домов/Квартир"
        context["houses"] = Home.objects.filter(user=request.user)
        if request.method == "POST":
            form = HomeForm(request.POST)
            if form.is_valid():
                home = Home(
                    name=form.data["Name"], city=form.data["City"], user=request.user
                )
                home.save()
                return redirect("/edit/")
            else:
                context["form"] = HomeForm()
        else:
            context["form"] = HomeForm()
        return render(request, "houses/houses.html", context)
    except Home.DoesNotExist:
        return handler404(request)


@login_required(login_url="/login/")
def add_room(request, home):
    """
    Страница добавления комнаты

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :param home: идентификатор дома
    :return: шаблон редактирования комнаты
    """
    try:
        house = Home.objects.get(id=home)
        if request.method == "POST" and house.user == request.user:
            form = RoomForm(request.POST)
            if form.is_valid() and check_key(form.data["key"]):
                room = Room(name=form.data["name"], house=house)
                room.save()
                generate_codes(room=room, key=form.data["key"])
                return redirect("/edit/" + str(home))
        return redirect("/edit/" + str(home))
    except Home.DoesNotExist:
        return handler404(request)


def products(request):
    """
    Страница покупки девайсов

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: шаблон покупки девайсов
    """
    context = get_base_context()
    magazine = Magazine.objects.filter()
    context["magazine"] = magazine
    return render(request, "products.html", context)


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
                room = Room.objects.filter(house=home)[0]
            except IndexError:
                return redirect("/panel/")
            personalization = Personalization.objects.get(user=request.user)
            personalization.room = room
            personalization.save()
            return redirect("/panel/")
        else:
            return handler403(request)
    except Home.DoesNotExist:
        return handler404(request)


@login_required(login_url="/login/")
def change_room(request, room_id):
    """
    Страница редактирования домов

    :param room_id: идентификатор комнаты, на которую требуется переключиться
    :type room_id: :class:`int`
    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: перенаправление на панель
    """
    try:
        room = Room.objects.get(id=room_id)
        if room.house.user == request.user:
            personalization = Personalization.objects.get(user=request.user)
            personalization.room = room
            personalization.save()
            return redirect("/panel/")
        else:
            return handler403(request)
    except Home.DoesNotExist:
        return handler404(request)


@login_required(login_url="/login/")
def create_license(request):
    """
    Страница создания кода активации для устройства

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: шаблон создания кода активации
    """
    context = get_base_context()
    context["title"] = "Создание Лицензии"
    if request.method == "POST":
        form = LicenseForm(request.POST)
        if form.is_valid():
            cmd = form.data["cmd"]
            context["code"] = new_license(str(cmd))
            context["form"] = LicenseForm()
        else:
            context["form"] = LicenseForm()
    else:
        context["form"] = LicenseForm()
    return render(request, "create_license.html", context)


@staff_member_required
def set_registration(request):
    """
    Страница включения/отключения регистрации(только для администраторов)

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: шаблон отключения регистрации
    """
    context = {}
    if request.method == "POST":
        try:
            signup = SignUp.objects.get(id=1)
            signup.active = not signup.active
            signup.save()
        except SignUp.DoesNotExist:
            signup = SignUp()
            signup.save()
        return redirect("/")
    else:
        context["form"] = HiddenForm()
        try:
            signup = SignUp.objects.get(id=1)
            if not signup.active:
                context["on"] = "ON"
                return render(request, "set_registration.html", context)
        except SignUp.DoesNotExist:
            signup = SignUp()
            signup.save()
        context["on"] = "OFF"
        return render(request, "set_registration.html", context)


@login_required(login_url='/login/')
def relay_room_off(request):
    """
    Страница выключения всех реле в комнате

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: панель с выключенными реле
    """
    relays = Relay.objects.filter(room=Personalization.objects.get(user=request.user).room)
    for relay in relays:
        relay.switched = False
        relay.save()
    return redirect('/panel/')


@login_required(login_url='/login/')
def relay_room_on(request):
    """
    Страница включения всех реле в комнате

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: панель с включенными реле
    """
    relays = Relay.objects.filter(room=Personalization.objects.get(user=request.user).room)
    for relay in relays:
        relay.switched = True
        relay.save()
    return redirect('/panel/')


@login_required(login_url='/login/')
def relay_house_on(request):
    """
    Страница включения всех реле в доме

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: панель с включенными реле
    """
    current = Personalization.objects.get(user=request.user).room.house
    for room in Room.objects.filter(house=current):
        relays = Relay.objects.filter(room=room)
        for relay in relays:
            relay.switched = True
            relay.save()
    return redirect('/panel/')


@login_required(login_url='/login/')
def relay_house_off(request):
    """
    Страница выключения всех реле в доме

    :param request: объект c деталями запроса
    :type request: :class:`django.http.HttpRequest`
    :return: панель с выключенными реле
    """
    current = Personalization.objects.get(user=request.user).room.house
    for room in Room.objects.filter(house=current):
        relays = Relay.objects.filter(room=room)
        for relay in relays:
            relay.switched = False
            relay.save()
    return redirect('/panel/')
