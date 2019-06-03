from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from home.apps.config.mail import email_contact
from home.views import get_base_context


class IndexTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse('main'))

    def test_index_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_index_context(self):
        self.assertEqual(self.response.context['title'], 'Главная страница - Alpha Home')


class ContextTest(TestCase):
    def test_context(self):
        self.context = get_base_context()
        self.assertEqual(self.context['phone'], '+7(964)578-53-44')
        self.assertEqual(self.context['email'], email_contact)


class AgreementTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse('agreement'))

    def test_agreement_response(self):
        self.assertEqual(self.response.status_code, 200)


class AuthorizeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse('login'))

    def test_authorize_response(self):
        self.assertEqual(self.response.status_code, 200)


class RegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse('signup'))

    def test_registration_response(self):
        self.assertEqual(self.response.status_code, 200)


class LogoutTest(TestCase):
    fixtures = ['test.json']

    def test_logout(self):
        self.client.login(username='vasya', password="promprog")
        response = self.client.get(reverse('panel'))
        self.assertEquals(response.status_code, 200)
        self.assertEqual(response.context['title'], "Панель Управления")
        self.client.logout()
        response = self.client.get(reverse('panel'))
        self.assertEquals(response.status_code, 302)


class AskTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse('support'))

    def test_ask_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_ask_context(self):
        self.assertEqual(self.response.context['title'], 'Обращение в тех.поддрежку')

    def test_context(self):
        self.context = get_base_context()
        self.assertEqual(self.context['phone'], '+7(964)578-53-44')
        self.assertEqual(self.context['email'], email_contact)


class SetPasswordTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse('recover_email_input'))

    def test_set_password_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_context(self):
        self.context = get_base_context()
        self.assertEqual(self.context['phone'], '+7(964)578-53-44')
        self.assertEqual(self.context['email'], email_contact)


class RecoverTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse('recover_email_input'))

    def test_recover_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_context(self):
        self.context = get_base_context()
        self.assertEqual(self.context['phone'], '+7(964)578-53-44')
        self.assertEqual(self.context['email'], email_contact)


class PanelTest(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.client = Client()
        user = User.objects.get(username="vasya")
        self.client.force_login(user)

    def test_panel_response(self):
        c = Client()
        response = c.get(reverse('panel'))
        self.assertEqual(response.status_code, 302)
        response = c.get(reverse('panel'), follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertIn(reverse('login'), last_url)

    def test_normal_panel(self):
        response = self.client.get(reverse('panel'))
        self.assertEqual(response.status_code, 200)

    def test_context(self):
        self.context = get_base_context()
        self.assertEqual(self.context['phone'], '+7(964)578-53-44')
        self.assertEqual(self.context['email'], email_contact)


class HelpTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse('help'))

    def test_help_response(self):
        self.assertEqual(self.response.status_code, 200)


class UploadTest(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.client = Client()
        user = User.objects.get(username="vasya")
        self.client.force_login(user)

    def test_upload_response(self):
        c = Client()
        response = c.get(reverse('upload_picture'))
        self.assertEqual(response.status_code, 302)
        response = c.get(reverse('upload_picture'), follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertIn(reverse('login'), last_url)

    def test_normal_upload(self):
        response = self.client.get(reverse('upload_picture'))
        self.assertEqual(response.status_code, 200)

    def test_context(self):
        self.context = get_base_context()
        self.assertEqual(self.context['phone'], '+7(964)578-53-44')
        self.assertEqual(self.context['email'], email_contact)


class ProfileTest(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.client = Client()
        user = User.objects.get(username="vasya")
        self.client.force_login(user)

    def test_profile_response(self):
        c = Client()
        response = c.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        response = c.get(reverse('profile'), follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertIn(reverse('login'), last_url)

    def test_normal_profile(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)


class ProductsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get(reverse('products'))

    def test_products_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_context(self):
        self.context = get_base_context()
        self.assertEqual(self.context['phone'], '+7(964)578-53-44')
        self.assertEqual(self.context['email'], email_contact)


class CreateTest(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.client = Client()
        user = User.objects.get(username="vasya")
        self.client.force_login(user)

    def test_create_response(self):
        c = Client()
        response = c.get(reverse('create_license'))
        self.assertEqual(response.status_code, 302)
        response = c.get(reverse('create_license'), follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertIn(reverse('login'), last_url)

    def test_normal_create(self):
        response = self.client.get(reverse('create_license'))
        self.assertEqual(response.status_code, 200)

    def test_context(self):
        self.context = get_base_context()
        self.assertEqual(self.context['phone'], '+7(964)578-53-44')
        self.assertEqual(self.context['email'], email_contact)


class SetRegistrationTest(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.client = Client()
        user = User.objects.get(username="vasya")
        self.client.force_login(user)

    def test_set_registration_response(self):
        c = Client()
        response = c.get(reverse('set_signup'))
        self.assertEqual(response.status_code, 302)
        response = c.get(reverse('set_signup'), follow=True)
        last_url, status_code = response.redirect_chain[-1]
        self.assertIn(reverse('login'), last_url)

    def test_set_registration_create(self):
        response = self.client.get(reverse('set_signup'))
        self.assertEqual(response.status_code, 200)


