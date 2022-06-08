from unittest import skip

from django.test import TestCase, Client
from. models import *

# Create your tests here.


def create_dummy_user(username:str, type_kor: str):
    korisnik = User()
    korisnik.username = username
    korisnik.set_password('kQ!:h9[T&B2,7*p{')
    korisnik.email = "dummyTest@dymmttesting.com"
    korisnik.type = type_kor
    korisnik.first_name = "Dummy"
    korisnik.last_name = "Test"
    korisnik.status = "A"
    korisnik.subscribed = "N"
    korisnik.save()
    return korisnik


class FormTests(TestCase):

    def test_username_changed_SSU18(self):
        c = Client()
        dummy = create_dummy_user("dummy8172387","U")
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        c.post("/change_personal_data/", data={
            'newUsername': 'newusername'
        })
        print(dummy.username)
        # ne detektuje promenu username-a
        success = c.login(username='newusername', password='kQ!:h9[T&B2,7*p{')
        self.assertTrue(success)
        #self.assertEqual(dummy.username, "newusername")
        #self.assertContains(response, 'newusername')


    def test_password_change_SSU18(self):
        c = Client()
        create_dummy_user("dummy8172387","U")
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        c.post("/change_personal_data/", data={
            'newPassword': 'kruska123',
            'confirm': 'kruska123'
        })
        success = c.login(username='dummy8172387', password='kruska123')
        self.assertTrue(success)

    def test_password_change_SSU18_wrong_confirm_password(self):
        c = Client()
        create_dummy_user("dummy8172387","U")
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        c.post("/change_personal_data/", data={
            'newPassword': 'kruska123',
            'confirm': 'kruska12'
        })
        success = c.login(username='dummy8172387', password='kruska123')
        self.assertFalse(success)


    def test_password_change_SSU18_too_short_password(self):
        c = Client()
        create_dummy_user("dummy8172387","U")
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        c.post("/change_personal_data/", data={
            'newPassword': 'aa',
            'confirm': 'aa'
        })
        success = c.login(username='dummy8172387', password='aa')
        self.assertFalse(success)


    def test_username_change_SSU18_too_short_username(self):
        c = Client()
        create_dummy_user("dummy8172387", "U")
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        c.post("/change_personal_data/", data={
            'newUsername': 'a',
        })
        success = c.login(username='a', password='kQ!:h9[T&B2,7*p{')
        self.assertFalse(success)

    def test_username_change_SSU18_too_long_username(self):
        c = Client()
        create_dummy_user("dummy8172387", "U")
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        c.post("/change_personal_data/", data={
            'newUsername': 'ajakajdjedeuhdurhfurrufhurhfurhfurhfuhrufhurhfurhfurhfurhfurhfuhrfrfrf',
        })
        success = c.login(username='ajakajdjedeuhdurhfurrufhurhfurhfurhfuhrufhurhfurhfurhfurhfurhfuhrfrfrf', password='kQ!:h9[T&B2,7*p{')
        self.assertFalse(success)

    def test_username_change_SSU18_existing_username(self):
        c = Client()
        create_dummy_user("dummy8172387", "U")
        dummy = create_dummy_user("jabuka","U")
        dummy.set_password("kruska123")
        dummy.save()
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        c.post("/change_personal_data/", data={
            'newUsername': 'jabuka',
        })
        success = c.login(username='jabuka', password='kQ!:h9[T&B2,7*p{')
        self.assertFalse(success)

    def test_firstName_change_SSU18(self):
        c = Client()
        create_dummy_user("dummy8172387", "U")
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        c.post("/change_personal_data/", data={
            'newFirstName': 'jabuka',
        })
        firstName = User.objects.get(username="dummy8172387").first_name
        self.assertEquals(firstName,'jabuka')

    def test_lastName_change_SSU18(self):
        c = Client()
        create_dummy_user("dummy8172387", "U")
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        c.post("/change_personal_data/", data={
            'newLastName': 'jabuka',
        })
        lastName = User.objects.get(username="dummy8172387").last_name
        self.assertEquals(lastName,'jabuka')

    def test_mail_change_SSU18(self):
        c = Client()
        create_dummy_user("dummy8172387", "U")
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        c.post("/change_personal_data/", data={
            'newMail': 'jabuka@kruska.com',
        })
        mail = User.objects.get(username="dummy8172387").email
        self.assertEquals(mail,'jabuka@kruska.com')

    def test_firstName_change_SSU18_too_short_firstName(self):
        c = Client()
        create_dummy_user("dummy8172387", "U")
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        c.post("/change_personal_data/", data={
            'newFirstName': 'a',
        })
        firstName = User.objects.get(username="dummy8172387").first_name
        self.assertNotEquals(firstName, 'a')

    def test_firstName_change_SSU18_too_long_firstName(self):
        c = Client()
        create_dummy_user("dummy8172387", "U")
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        c.post("/change_personal_data/", data={
            'newFirstName': 'addddddddddddddededeeeeeeeeeeeeedededededdeddede',
        })
        firstName = User.objects.get(username="dummy8172387").first_name
        self.assertNotEquals(firstName, 'addddddddddddddededeeeeeeeeeeeeedededededdeddede')

    def test_firstName_change_SSU18_too_short_lastName(self):
        c = Client()
        create_dummy_user("dummy8172387", "U")
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        c.post("/change_personal_data/", data={
            'newLastName': 'a',
        })
        lastName = User.objects.get(username="dummy8172387").last_name
        self.assertNotEquals(lastName, 'a')

    def test_firstName_change_SSU18_too_long_lastName(self):
        c = Client()
        create_dummy_user("dummy8172387", "U")
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        c.post("/change_personal_data/", data={
            'newLastName': 'adedefrfrfr45t6hh6546h444444444444444444444444444444444444',
        })
        lastName = User.objects.get(username="dummy8172387").last_name
        self.assertNotEquals(lastName, 'adedefrfrfr45t6hh6546h444444444444444444444444444444444444')


    def test_mail_change_SSU18_bad_mail(self):
        c = Client()
        create_dummy_user("dummy8172387", "U")
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        c.post("/change_personal_data/", data={
            'newMail': 'jabuka',
        })
        mail = User.objects.get(username="dummy8172387").email
        self.assertNotEquals(mail, 'jabuka')