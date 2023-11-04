from django.test import SimpleTestCase
from account_app import views
from django.urls import reverse, resolve


class TestUrl(SimpleTestCase):
    def test_login(self):
        url = reverse('account:login_page')
        self.assertEqual(resolve(url).func.view_class, views.Login)

    def test_register(self):
        url = reverse('account:register_page')
        self.assertEqual(resolve(url).func.view_class, views.Register)

    def test_user_add_api(self):
        url = reverse('account:UserAdd_api')
        self.assertEqual(resolve(url).func.view_class, views.UserAddView)
