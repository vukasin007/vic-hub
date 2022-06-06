from django.test import TestCase, Client
from. models import *

# Create your tests here.


def create_dummy_user(type_kor: str):
    korisnik = User()
    korisnik.username = "dummy8172387"
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

    def test_username_changed(self):
        c = Client()
        dummy = create_dummy_user("U")
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        response = c.post("", data={
            'newUsername': 'newusername'
        })
        print(dummy.username)
        # ne detektuje promenu username-a
        c.login(username='newusername', password='kQ!:h9[T&B2,7*p{')
        self.assertEqual(dummy.username, "newusername")
        self.assertContains(response, 'newusername')
