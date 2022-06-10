from unittest import skip

from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.urls import reverse

from .models import *

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

def create_dummy_joke():
    korisnik = Joke()
    korisnik.content= "glup vic"
    korisnik.title="naslov"
    korisnik.status="A"

    aa=create_dummy_user("kor","M")

    korisnik.id_user_created = aa
    korisnik.id_user_reviewed = aa
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


    def test_remove_mod_privileges_SSU19(self):
        dummy=create_dummy_user("dummy8172387", "M")
        admin=create_dummy_user("admin", "A")
        id = dummy.id_user
        self.client.force_login(user=admin)

        url = reverse("remove_mod", args=(id,))
        response = self.client.get(path=url)

        self.assertEquals(response.status_code,200)

        type = User.objects.get(username="dummy8172387").type
        self.assertNotEquals(type, 'M')

    def test_remove_mod_privileges_SSU19_fail_not_admin(self):
        dummy = create_dummy_user("dummy8172387", "M")
        not_admin = create_dummy_user("admin", "M")
        id = dummy.id_user
        self.client.force_login(user=not_admin)

        url = reverse("remove_mod", args=(id,))
        self.client.get(path=url)

        type = User.objects.get(username="dummy8172387").type
        self.assertEquals(type, 'M')

    def test_moderator_approve_SSU17(self):
        dummy = create_dummy_user("dummy8172387", "U")
        admin = create_dummy_user("admin", "A")

        self.client.force_login(user=dummy)

        url = reverse("request_mod")
        self.client.get(path=url)

        request=Request.objects.get(id_user=dummy)
        id = request.id_request

        self.client.logout()

        self.client.force_login(user=admin)
        url = reverse("accept_mod_request", args=(id,))
        r=self.client.get(path=url)
        self.assertEquals(r.status_code,200)

        type = User.objects.get(username="dummy8172387").type
        self.assertEquals(type, 'M')

    def test_moderator_reject_SSU17(self):
        dummy = create_dummy_user("dummy8172387", "U")
        admin = create_dummy_user("admin", "A")
        id=dummy.id_user

        self.client.force_login(user=dummy)
        url = reverse("request_mod")
        self.client.get(path=url)

        self.client.logout()

        self.client.force_login(user=admin)
        url = reverse("reject_mod_request", args=(id,))
        self.client.get(path=url)

        type = User.objects.get(username="dummy8172387").type
        self.assertEquals(type, 'U')

    def test_SSU17_fail_not_admin(self):
        dummy = create_dummy_user("dummy8172387", "U")
        notadmin = create_dummy_user("admin", "U")
        id=dummy.id_user

        self.client.force_login(user=dummy)
        url = reverse("request_mod")
        self.client.get(path=url)

        self.client.logout()

        self.client.force_login(user=notadmin)
        url = reverse("accept_mod_request", args=(id,))
        self.client.get(path=url)

        type = User.objects.get(username="dummy8172387").type
        self.assertEquals(type, 'U')

    def test_moderator_request_SSU14(self):
        dummy = create_dummy_user("dummy8172387", "U")

        before = Request.objects.all().count()

        self.client.force_login(user=dummy)

        url = reverse("request_mod")
        r=self.client.get(path=url,follow=True)
        self.assertContains(r,'Uspesno formiran zahtev za moderatora!' , html=True)

        after = Request.objects.all().count()

        self.assertEquals(before+1, after)

    def test_moderator_request_SSU14_again_request(self):
        dummy = create_dummy_user("dummy8172387", "U")
        zero = Request.objects.all().count()

        self.client.force_login(user=dummy)

        url = reverse("request_mod")
        self.client.get(path=url)

        one = Request.objects.all().count()

        url = reverse("request_mod")
        r=self.client.get(path=url,follow=True)
        self.assertContains(r, 'Vec ste poslali zahtev', html=True)

        two = Request.objects.all().count()

        self.assertTrue(zero+1==one)
        self.assertEquals(one,two)

    def test_moderator_request_SSU14_already_mod(self):
        dummy = create_dummy_user("dummy8172387", "M")
        zero = Request.objects.all().count()

        self.client.force_login(user=dummy)

        url = reverse("request_mod")
        r=self.client.get(path=url,follow=True)
        self.assertContains(r,"Nemate pravo na ovu akciju",html=True)

        one = Request.objects.all().count()

        self.assertEquals(one, zero)

    def test_unsubscribe_from_bilten_SSU16(self):
        dummy = create_dummy_user("dummy8172387", "M")
        dummy.subscribed= "Y"

        self.client.force_login(user=dummy)

        url = reverse("unsubscribe_from_bilten")
        r = self.client.get(path=url, follow=True)
        self.assertContains(r, "Uspesna odjava sa biltena!", html=True)

        self.assertEquals(User.objects.get(username="dummy8172387").subscribed, "N")

    def test_subscribe_to_bilten_SSU13(self):
        dummy = create_dummy_user("dummy8172387", "M")

        self.client.force_login(user=dummy)

        url = reverse("subscribe_to_bilten")
        r=self.client.get(path=url, follow=True)
        self.assertContains(r,"Uspesna prijava na bilten!", html=True)

        self.assertEquals(User.objects.get(username="dummy8172387").subscribed, "Y")


    def test_logout_SSU15(self):
        dummy = create_dummy_user("dummy8172387", "M")

        self.client.force_login(user=dummy)

        url = reverse("logout")
        r = self.client.get(path=url, follow=True)
        self.assertContains(r,"Uspesna odjava!", html=True)


    def test_category_add_SSU11(self):
        dummy = create_dummy_user("dummy8172387", "M")
        self.client.force_login(user=dummy)
        before = Category.objects.all().count()

        url = reverse("add_category")
        r = self.client.post(path=url, follow=True, data={
            "Naziv": "Mujo i Fata"
        })
        self.assertContains(r,'Uspesno kreiranje nove kategorije!',html=True)

        after = Category.objects.all().count()

        self.assertEquals(before+1,after)

    def test_category_add_SSU11_empty_title(self):
        dummy = create_dummy_user("dummy8172387", "M")
        self.client.force_login(user=dummy)
        before = Category.objects.all().count()

        url = reverse("add_category")
        r = self.client.post(path=url, follow=True, data={
            "Naziv": ""
        })

        after = Category.objects.all().count()

        self.assertEquals(before,after)

    def test_category_add_SSU11_basic_user(self):
        dummy = create_dummy_user("dummy8172387", "U")
        self.client.force_login(user=dummy)
        before = Category.objects.all().count()

        url = reverse("add_category")
        r = self.client.post(path=url, follow=True, data={
            "Naziv": "Kateg"
        })

        after = Category.objects.all().count()

        self.assertEquals(before, after)
        
    def test_login_SSU1_successful_login(self):
        c = Client()
        dummy = create_dummy_user("dummy8172387", "U")
        c.login(username="dummy8172387", password="kQ!:h9[T&B2,7*p{")
        response = c.post('/login/')
        self.assertRedirects(response, '/')

    def test_login_SSU1_empty_username(self):
        c = Client()
        dummy = create_dummy_user("dummy8172387", "U")
        c.login(username="", password="kQ!:h9[T&B2,7*p{")
        response = c.post('/login/')
        self.assertContains(response, 'Prijava nije uspela. Podaci su nevalidni.', html=True)

    def test_login_SSU1_empty_password(self):
        c = Client()
        dummy = create_dummy_user("dummy8172387", "U")
        c.login(username="dummy8172387", password="")
        response = c.post('/login/')
        self.assertContains(response, 'Prijava nije uspela. Podaci su nevalidni.', html=True)

    def test_login_SSU1_username_does_not_exist(self):
        c = Client()
        dummy = create_dummy_user("dummy8172387", "U")
        c.login(username="dummy8172387123", password="kQ!:h9[T&B2,7*p{")
        response = c.post('/login/')
        self.assertContains(response, 'Prijava nije uspela. Podaci su nevalidni.', html=True)

    def test_login_SSU1_wrong_password(self):
        c = Client()
        dummy = create_dummy_user("dummy8172387", "U")
        c.login(username="dummy8172387", password="kJ!:h9[T&B2,7*p{")
        response = c.post('/login/')
        self.assertContains(response, 'Prijava nije uspela. Podaci su nevalidni.', html=True)

    def test_register_SSU2_successful_registration(self):
        c = Client()
        g = Group(name="basic")
        g.save()
        response = c.post('/register/', data={
            'username': 'dummy8172387',
            'password1': 'kQ!:h9[T&B2,7*p{',
            'password2': 'kQ!:h9[T&B2,7*p{',
            'first_name': 'Dummy',
            'last_name': 'Test',
            'email': 'dummyTest@dymmttesting.com',
            'date_of_birth': '2000-10-10'
        })
        success = c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        self.assertTrue(success)

    def test_register_SSU2_empty_username(self):
        c = Client()
        g = Group(name="basic")
        g.save()
        response = c.post('/register/', data={
            'username': '',
            'password1': 'kQ!:h9[T&B2,7*p{',
            'password2': 'kQ!:h9[T&B2,7*p{',
            'first_name': 'Dummy',
            'last_name': 'Test',
            'email': 'dummyTest@dymmttesting.com',
            'date_of_birth': '2000-10-10'
        })
        success = c.login(username='', password='kQ!:h9[T&B2,7*p{')
        self.assertFalse(success)

    def test_register_SSU2_empty_password(self):
        c = Client()
        g = Group(name="basic")
        g.save()
        response = c.post('/register/', data={
            'username': 'dummy8172387',
            'password1': '',
            'password2': 'kQ!:h9[T&B2,7*p{',
            'first_name': 'Dummy',
            'last_name': 'Test',
            'email': 'dummyTest@dymmttesting.com',
            'date_of_birth': '2000-10-10'
        })
        success = c.login(username='dummy8172387', password='')
        self.assertFalse(success)

    def test_register_SSU2_wrong_confirm_password(self):
        c = Client()
        g = Group(name="basic")
        g.save()
        response = c.post('/register/', data={
            'username': 'dummy8172387',
            'password1': 'kQ!:h9[T&B2,7*p{',
            'password2': 'kQ!:h9[P&B2,7*p{',
            'first_name': 'Dummy',
            'last_name': 'Test',
            'email': 'dummyTest@dymmttesting.com',
            'date_of_birth': '2000-10-10'
        })
        success = c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        self.assertFalse(success)

    def test_register_SSU2_username_exists(self):
        c = Client()
        g = Group(name="basic")
        g.save()
        dummy = create_dummy_user("dummy8172387","U")
        response = c.post('/register/', data={
            'username': 'dummy8172387',
            'password1': 'kq!:h9[T&B2,7*p{',
            'password2': 'kq!:h9[T&B2,7*p{',
            'first_name': 'Dummy',
            'last_name': 'Test',
            'email': 'dummyTest@dymmttesting.com',
            'date_of_birth': '2000-10-10'
        })
        success = c.login(username='dummy8172387', password='kq!:h9[T&B2,7*p{')
        self.assertFalse(success)

    def test_add_joke_SSU3_successful(self):
        c = Client()
        dummy = create_dummy_user("dummy8172387", "U")
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        response = c.post('/add_joke/', data={
            "joke_content": "glup vic",
            "joke_title": "naslov"
        })
        self.assertContains(response, 'Uspesno ste poslali vic na proveru', html=True)

    def test_add_joke_SSU3_title_missing(self):
        c = Client()
        dummy = create_dummy_user("dummy8172387", "U")
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        response = c.post('/add_joke/', data={
            "joke_content": "glup vic",
            "joke_title": ""
        })
        response = c.get('/add_joke/', follow=True)
        self.assertContains(response, 'Niste uneli naslov vica', html=True)

    def test_add_joke_SSU3_content_missing(self):
        c = Client()
        dummy = create_dummy_user("dummy8172387", "U")
        c.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        response = c.post('/add_joke/', data={
            "joke_content": "",
            "joke_title": "naslov"
        })
        response = c.get('/add_joke/', follow=True)
        self.assertContains(response, 'Niste uneli sadrzaj vica', html=True)

    def test_register_by_admin_SSU4_create_basic_user(self):
        dummy_admin = create_dummy_user('admin', 'A')
        self.client.login(username='admin', password='kQ!:h9[T&B2,7*p{')
        Group(name='basic').save()
        self.client.post('/register_admin/', data={
            'username': 'dummy8172387',
            'password1': 'kQ!:h9[T&B2,7*p{',
            'password2': 'kQ!:h9[T&B2,7*p{',
            'first_name': 'Dummy',
            'last_name': 'Test',
            'email': 'dummyTest@dymmttesting.com',
            'date_of_birth': '2000-10-10',
            'type': 'basic'
        })
        self.assertTrue(User.objects.get(username='dummy8172387').groups.filter(name='basic').exists())

    def test_register_by_admin_SSU4_create_moderator(self):
        dummy_admin = create_dummy_user('admin', 'A')
        self.client.login(username='admin', password='kQ!:h9[T&B2,7*p{')
        Group(name='moderator').save()
        self.client.post('/register_admin/', data={
            'username': 'dummy8172387',
            'password1': 'kQ!:h9[T&B2,7*p{',
            'password2': 'kQ!:h9[T&B2,7*p{',
            'first_name': 'Dummy',
            'last_name': 'Test',
            'email': 'dummyTest@dymmttesting.com',
            'date_of_birth': '2000-10-10',
            'type': 'moderator'
        })
        self.assertTrue(User.objects.get(username='dummy8172387').groups.filter(name='moderator').exists())

    def test_delete_user_admin_SSU5_successful(self):
        dummy_user = create_dummy_user('dummy8172387', 'U')
        dummy_admin = create_dummy_user('admin', 'A')
        self.client.login(username='admin', password='kQ!:h9[T&B2,7*p{')
        self.client.get(f'/delete_user_admin/{dummy_user.id_user}')
        response = self.client.get('/admin_all_users/')
        self.assertContains(response, f'Korisnik {dummy_user.username} je uspešno obrisan.', html=True)

    def test_delete_joke_SSU6_successful(self):
        dummy_joke = create_dummy_joke()
        self.client.login(username='kor', password='kQ!:h9[T&B2,7*p{')

        comment = Comment()
        comment.id_joke = dummy_joke
        comment.id_user = User.objects.get(username='kor')
        comment.ordinal_number = 1
        comment.status = 'A'
        comment.save()

        self.client.post(f'/delete_joke/{dummy_joke.id_joke}')
        dummy_joke.refresh_from_db()
        comment.refresh_from_db()
        self.assertEquals(dummy_joke.status, 'D')
        self.assertEquals(comment.status, 'D')

    def test_delete_joke_SSU6_method_is_get(self):
        dummy_joke = create_dummy_joke()
        self.client.login(username='kor', password='kQ!:h9[T&B2,7*p{')
        response = self.client.get(f'/delete_joke/{dummy_joke.id_joke}')
        self.assertContains(response, 'Method nije POST', html=True)

    def test_delete_comment_SSU7_successful(self):
        dummy_joke = create_dummy_joke()
        self.client.login(username='kor', password='kQ!:h9[T&B2,7*p{')

        comment = Comment()
        comment.id_joke = dummy_joke
        comment.id_user = User.objects.get(username='kor')
        comment.ordinal_number = 1
        comment.status = 'A'
        comment.save()

        self.client.post(f'/delete_comment/{comment.id_comment}', data={
            'id_joke': dummy_joke.id_joke
        })
        comment.refresh_from_db()
        self.assertEquals(comment.status, 'D')

    def test_delete_comment_SSU7_basic_user(self):
        dummy_user = create_dummy_user('dummy8172387', 'U')
        self.client.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        response = self.client.post(f'/delete_comment/{dummy_user.id_user}')
        self.assertContains(response, 'Nemate privilegije.', html=True)

    def test_delete_comment_SSU7_method_is_get(self):
        dummy_joke = create_dummy_joke()
        self.client.login(username='kor', password='kQ!:h9[T&B2,7*p{')
        response = self.client.get('/delete_comment/1')
        self.assertContains(response, 'Method nije POST', html=True)

    def test_accept_joke_SSU8_successful(self):
        dummy_joke = create_dummy_joke()
        dummy_joke.status = 'P'
        dummy_joke.save()

        self.client.login(username='kor', password='kQ!:h9[T&B2,7*p{')
        self.client.post(f'/accept_joke/{dummy_joke.id_joke}', data={
            'kategorija': ['']
        })

        dummy_joke.refresh_from_db()
        self.assertEquals(dummy_joke.status, 'A')

    def test_accept_joke_SSU8_no_categories(self):
        dummy_joke = create_dummy_joke()
        self.client.login(username='kor', password='kQ!:h9[T&B2,7*p{')
        self.client.post(f'/accept_joke/{dummy_joke.id_joke}', data={
            'kategorija': []
        })
        response = self.client.get(f'/choose_category/{dummy_joke.id_joke}')
        self.assertContains(response, 'Niste odabrali kategoriju', html=True)

    def test_reject_joke_SSU8_successful(self):
        dummy_joke = create_dummy_joke()
        self.client.login(username='kor', password='kQ!:h9[T&B2,7*p{')
        self.client.post(f'/reject_joke/{dummy_joke.id_joke}')
        dummy_joke.refresh_from_db()
        self.assertEquals(dummy_joke.status, 'R')

    def test_grade_joke_SSU9_new_grade(self):
        dummy_joke = create_dummy_joke()
        dummy_user = create_dummy_user('dummy8172387', 'U')
        self.client.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')
        self.client.post(f'/grade_joke/{dummy_joke.id_joke}', data={
            'grade': '4'
        })
        new_grade = Grade.objects.filter(id_joke=dummy_joke).filter(id_user=dummy_user).first()
        self.assertEquals(new_grade.grade, 4)

    def test_grade_joke_SSU9_change_grade(self):
        dummy_joke = create_dummy_joke()
        dummy_user = create_dummy_user('dummy8172387', 'U')
        self.client.login(username='dummy8172387', password='kQ!:h9[T&B2,7*p{')

        self.client.post(f'/grade_joke/{dummy_joke.id_joke}', data={
            'grade': '4'
        })
        new_grade = Grade.objects.filter(id_joke=dummy_joke).filter(id_user=dummy_user).first()
        self.assertEquals(new_grade.grade, 4)

        self.client.post(f'/grade_joke/{dummy_joke.id_joke}', data={
            'grade': '5'
        })
        changed_grade = Grade.objects.filter(id_joke=dummy_joke).filter(id_user=dummy_user).first()
        self.assertEquals(changed_grade.grade, 5)

    def test_grade_joke_SSU9_user_posted_the_joke(self):
        dummy_joke = create_dummy_joke()
        self.client.login(username='kor', password='kQ!:h9[T&B2,7*p{')
        self.client.post(f'/grade_joke/{dummy_joke.id_joke}', data={
            'grade': '5'
        })
        response = self.client.get(f'/joke/{dummy_joke.id_joke}', follow=True)
        self.assertContains(response, 'Ne možete oceniti svoj vic', html=True)

    def test_grade_joke_SSU9_method_is_get(self):
        dummy_joke = create_dummy_joke()
        self.client.login(username='kor', password='kQ!:h9[T&B2,7*p{')
        response = self.client.get(f'/grade_joke/{dummy_joke.id_joke}')
        self.assertContains(response, 'Method nije POST', html=True)

    def test_add_comment_SSU10_successful(self):
        dummy_joke = create_dummy_joke()
        self.client.login(username='kor', password='kQ!:h9[T&B2,7*p{')
        self.client.post(f'/add_comment/{dummy_joke.id_joke}', data={
            'comment_content': 'Test comment'
        })
        response = self.client.get(f'/joke/{dummy_joke.id_joke}', follow=True)
        self.assertContains(response, 'Uspesno ste dodali komentar', html=True)

    def test_add_comment_SSU10_comment_missing(self):
        dummy_joke = create_dummy_joke()
        self.client.login(username='kor', password='kQ!:h9[T&B2,7*p{')
        self.client.post(f'/add_comment/{dummy_joke.id_joke}', data={
            'comment_content': ''
        })
        response = self.client.get(f'/add_comment/{dummy_joke.id_joke}', follow=True)
        self.assertContains(response, 'Niste uneli komentar', html=True)
