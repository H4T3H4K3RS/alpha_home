from django import forms
from django.contrib.auth.models import User
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


class RecoverForm(forms.Form):
    """
    Форма восстановления пользователя :func:`home.views.recover`

    :param email: поле ввода email'a
    :param recaptcha: поле recaptchav3
    """
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': 'materialRegisterFormEmail'
            }
        )
    )
    recaptcha = ReCaptchaField(widget=ReCaptchaWidget(), required=True)


class RecoverCodeForm(forms.Form):
    """
    Форма для восстановления профиля, ввод кода :func:`home.views.recover`

    :param code: поле ввода кода от 100000 до 999999, полученный по email
    """
    code = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'id': 'materialNumber',
                'value': '100000'
            },
        ),
        min_value=100000,
        max_value=999999
    )
    recaptcha = ReCaptchaField(widget=ReCaptchaWidget(), required=True)


class NewPasswordForm(forms.Form):
    """
    Форма ввода нового пароля :func:`home.views.set_password`

    :param password: поле ввода новый пароль
    :param password2: поле ввода потверждение нового пароля
    """
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'materialRegisterFormPassword'
            }
        ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'id': 'materialRegisterFormPassword2'
        }
    ))

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class LoginForm(forms.Form):
    """
    Форма для авторизации :func:`home.views.login_page`

    :param login: поле ввода логина
    :param password: поле ввода пароля
    """
    login = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'materialLoginFormEmail'
        }
    ), required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'id': 'materialLoginFormPassword'
        }
    ))
    recaptcha = ReCaptchaField(widget=ReCaptchaWidget(), required=True)


class UserRegistrationForm(forms.ModelForm):
    """
    Форма для регистрации :func:`home.views.register_page`

    :param password: поле ввода пароля
    :param password2: поле ввода потверждающего пароля
    :param username: поле ввода никнейма
    :param last_name: поле ввода фамилии
    :param first_name: поле ввода имени
    """
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'materialRegisterFormPassword'
            }
        ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'id': 'materialRegisterFormPassword2'
        }
    ))
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'materialRegisterFormUsername'
        }
    ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': 'materialRegisterFormEmail'
            }
        )
    )

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'materialRegisterFormLastName'
        }
    ))
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'materialRegisterFormFirstName'
        }
    ))
    recaptcha = ReCaptchaField(widget=ReCaptchaWidget(), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'first_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class AskForm(forms.Form):
    """
    Форма для создания вопроcа :func:`home.views.ask`

    :param Name: поле ввода имени
    :param Email: поле ввода email'a
    :param Question: поле ввода вопроса
    :param recaptcha: recaptcha v3
    """
    Name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "materialContactFormName",
            }
        ),
        required=True
    )
    Email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "materialContactFormEmail",
            }
        ),
        required=True
    )
    Question = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": 'form-control md-textarea',
                'id': 'materialContactFormMessage',
                'rows': '3',
            }
        ),
        required=True
    )
    recaptcha = ReCaptchaField(widget=ReCaptchaWidget(), required=True)


class HomeForm(forms.Form):
    """
    Форма ввода данных дома

    :param Name: поле ввода названия
    :param city: поле ввода города
    :param recaptcha: recaptcha v3
    """
    Name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "id": "name",
                "placeholder": "Название"
            }
        ),
        required=True
    )

    City = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "id": "city",
                "placeholder": "Город"
            }
        ),
        required=True
    )
    recaptcha = ReCaptchaField(widget=ReCaptchaWidget(), required=True)


class EditHomeForm(forms.Form):
    """
    Форма редактирования дома/квартиры

    :param Name: название
    :param City: город
    :param recaptcha: recapctha v3
    """
    Name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "id": "name",
                "placeholder": "Название"
            }
        ),
        required=True
    )

    City = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "id": "city",
                "placeholder": "Город"
            }
        ),
        required=True
    )


class HiddenForm(forms.Form):
    """
    Невидимая форма для подтверждения удаления

    :param delete: скрытое поле
    """
    delete = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                "id": "delete"
            }
        )
    )


class RoomForm(forms.Form):
    """
    Форма создания новой комнаты

    :param name: название комнаты
    :param key: ключ активации
    :param recaptcha: recapctha v3
    """
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Название",
            }
        ),
        required=True
    )
    key = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ключ Активации",
            }
        ),
        required=True
    )
    recaptcha = ReCaptchaField(widget=ReCaptchaWidget(), required=True)


class EditRoomForm(forms.Form):
    """
    Форма изменения данных комнаты

    :param name: название комнаты
    """
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "id": "name",
                "placeholder": "Название",
            }
        )
    )


class UploadImageForm(forms.Form):
    """
    Форма загрузки файлов

    :param file: загрузка файла
    """
    file = forms.FileField(widget=forms.FileInput(
        attrs={'accept': 'application/image'}))


class LicenseForm(forms.Form):
    """
    Форма для создания лицензионных ключей
    :param cmd: какие датчики присутствуют в лицензии
    """
    cmd = forms.IntegerField(
        max_value=4321,
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                "id": "cmd",
                "placeholder": "Команда",
            }
        )
    )
    recaptcha = ReCaptchaField(widget=ReCaptchaWidget(), required=True)


class ProfileForm(forms.Form):
    """
    Форма для регистрации :func:`home.views.profile`

    :param password: поле ввода пароля
    :param password2: поле ввода потверждающего пароля
    :param username: поле ввода никнейма
    :param last_name: поле ввода фамилии
    :param first_name: поле ввода имени
    """
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'id': 'password',
                'placeholder': 'Новый пароль'
            },
        ),
        required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'id': 'password2',
            'placeholder': 'Подтвердите пароль'
        }
    ),
        required=False)
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'username',
            'placeholder': 'Никнейм'
        }
    ),
        required=True)
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'id': 'email',
                'placeholder': 'your@email.com'
            }
        ),
        required=True
    )

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'last_name',
            'placeholder': 'Фамилия'
        },
    ),
        required=True)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'first_name',
            'placeholder': 'Имя'
        }
    ),
        required=True)
    recaptcha = ReCaptchaField(widget=ReCaptchaWidget(), required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'last_name', 'first_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
