from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from account_app.forms import LoginForm, RegisterForm
from account_app.serializers import UserSerializer


class TestUserLoginView(TestCase):
    def setUp(self):
        User.objects.create_user(username='root', email='root@example.com', password='root1234')
        self.client = Client()

    def test_user_login_GET_notAuthenticated(self):
        response = self.client.get(reverse('account:login_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_app/login.html')
        self.failUnless(response.context['form'], LoginForm)

    def test_user_login_GET_authenticated(self):
        self.client.login(username='root', email='root@example.com', password='root1234')
        response = self.client.get(reverse('account:login_page'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('quiz:quiz_page'))

    def test_user_login_POST_valid(self):
        response = self.client.post(reverse('account:login_page'), data={'fullname': 'root', 'password': 'root1234'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('quiz:quiz_page'))

    def test_user_login_POST_invalid(self):
        response = self.client.post(reverse('account:login_page'), data={'fullname': 'rot', 'password': 'rot1234'})
        self.failIf(response.context['form'].is_valid())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_app/login.html')
        self.failUnless(response.context['form'], LoginForm)
        self.assertFormError(form=response.context['form'], field='fullname', errors=['Invalid User Data'])


class TestUserRegisterView(TestCase):
    def setUp(self):
        User.objects.create_user(username='root', email='root@example.com', password='root1234')
        self.client = Client()

    def test_user_register_GET_notAuthenticated(self):
        response = self.client.get(reverse('account:register_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_app/register.html')
        self.failUnless(response.context['form'], RegisterForm)

    def test_user_register_GET_authenticated(self):
        self.client.login(username='root', email='root@example.com', password='root1234')
        response = self.client.get(reverse('account:register_page'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('quiz:quiz_page'))

    def test_user_register_POST_valid(self):
        register_form_data = {
            'first_name': 'Aron',
            'last_name': 'Sadegh',
            'email': 'aronesadegh@gmail.com',
            'password': 'aron12345',
            'conf_pass': 'aron12345',
        }
        form = RegisterForm(register_form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('account:register_page'), data=register_form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('quiz:quiz_page'))
        self.assertEqual(User.objects.count(), 2)

    def test_user_register_POST_invalid(self):
        register_form_data = {
            'first_name': 'Aron',
            'last_name': 'Sadegh',
            'email': 'aronesadegh@gmail.com',
            'password': 'aron123456',
            'conf_pass': 'aron12345'
        }
        form = RegisterForm(register_form_data)
        self.failIf(form.is_valid())
        response = self.client.post(reverse('account:register_page'), data=register_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_app/register.html')
        self.failUnless(response.context['form'], RegisterForm)
        self.assertFormError(form=response.context['form'], field='password', errors=['Passwords are not the same !!'])
        self.assertEqual(User.objects.count(), 1)


class TestApiUserAddView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.super_user = User.objects.create_superuser(username='root2', email='root2@example.com', password='root21234')

    def test_create_user_without_authentication(self):
        response = self.client.post(reverse('account:UserAdd_api'), data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_user_without_staffPermission(self):
        user = User.objects.create_user(username='root', email='root@example.com', password='root1234')
        self.client.force_authenticate(user=user)
        response = self.client.post(reverse('account:UserAdd_api'), data={}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_valid_data(self):
        user_data = {
            'username': 'aron.s',
            'first_name': 'Aron',
            'last_name': 'Sadegh',
            'email': 'aronesadegh@gmail.com',
            'password': 'aron1234',
        }
        serializer = UserSerializer(data=user_data)
        self.assertTrue(serializer.is_valid())
        self.client.force_authenticate(user=self.super_user)
        response = self.client.post(reverse('account:UserAdd_api'), data=user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'response': user_data})
        self.assertEqual(User.objects.count(), 2)

    def test_create_user_invalid_data(self):
        user_data = {
            'username': 'aron.s',
            'first_name': 'Aron',
            'last_name': 'Sadegh',
            'password': 'aron1234',
        }
        serializer = UserSerializer(data=user_data)
        self.failIf(serializer.is_valid())
        self.client.force_authenticate(user=self.super_user)
        response = self.client.post(reverse('account:UserAdd_api'), data=user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'email': ['این مقدار لازم است.']})
        self.assertEqual(User.objects.count(), 1)
