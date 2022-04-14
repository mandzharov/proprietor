from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import exceptions

from proprietor.register.models import Profile, CountryCodes


UserModel = get_user_model()

USER_1_DATA = {
    'email': 'm@m.com',
    'password': 'admin123123'
}

USER_2_DATA = {
    'email': 'm2@m.com',
    'password': 'admin123123'
}


class ProfileDetailsViewTests(TestCase):

    def setUp(self):
        self.user_1 = UserModel.objects.create_user(email=USER_1_DATA['email'])
        self.user_1.set_password(USER_1_DATA['password'])
        self.user_1.save()
        self.PHONE_CODE = CountryCodes.objects.create(name='BG', code='+359')
        self.PROFILE_DATA = {
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'birth_date': date(1999, 2, 23),
            'gender': 'M',
            'phone_code': self.PHONE_CODE,
            'phone': '888888888',
            'user': self.user_1
        }
        self.profile = Profile.objects.create(**self.PROFILE_DATA)
        self.profile.save()

        self.user_2 = UserModel.objects.create_user(email=USER_2_DATA['email'])
        self.user_2.set_password(USER_2_DATA['password'])
        self.user_2.save()

    def test_view_correct_profile(self):
        self.client.login(**USER_1_DATA)
        response = self.client.get(reverse('view profile', kwargs={'pk': self.user_1.pk}))
        self.assertEqual(self.user_1, response.context['user'])
        
    def test_view_incorrect_profile_404(self):
        self.client.login(**USER_1_DATA)
        response = self.client.get(reverse('view profile', kwargs={'pk': self.user_2.pk}))
        self.assertEqual(404, response.status_code)


class EditProfileViewTests(TestCase):

    def setUp(self):
        self.user_1 = UserModel.objects.create_user(email=USER_1_DATA['email'])
        self.user_1.set_password(USER_1_DATA['password'])
        self.user_1.save()
        self.PHONE_CODE = CountryCodes.objects.create(name='BG', code='+359')
        self.PROFILE_DATA = {
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'birth_date': date(1999, 2, 23),
            'gender': 'M',
            'phone_code': self.PHONE_CODE,
            'phone': '888888888',
            'user': self.user_1
        }
        self.profile = Profile.objects.create(**self.PROFILE_DATA)
        self.profile.save()

        self.user_2 = UserModel.objects.create_user(email=USER_2_DATA['email'])
        self.user_2.set_password(USER_2_DATA['password'])
        self.user_2.save()

    def test_edit_profile_success(self):
        PROFILE_EDIT_DATA = {
            'first_name': 'Ivan',
            'middle_name': '',
            'last_name': 'Ivanov',
            'birth_date': date(1999, 2, 23),
            'gender': 'M',
            'phone_code': self.PHONE_CODE.pk,
            'phone': '999999999',
        }
        self.client.login(**USER_1_DATA)
        response = self.client.post(reverse('edit profile', kwargs={'pk': self.user_1.pk}), PROFILE_EDIT_DATA)
        self.assertEqual(302, response.status_code)
        self.user_1.refresh_from_db()
        self.assertEqual('999999999', self.user_1.profile.phone)

    def test_edit_wrong_profile_404(self):
        PROFILE_EDIT_DATA = {
            'first_name': 'Ivan',
            'middle_name': '',
            'last_name': 'Ivanov',
            'birth_date': date(1999, 2, 23),
            'gender': 'M',
            'phone_code': self.PHONE_CODE.pk,
            'phone': '999999999',
        }
        self.client.login(**USER_1_DATA)
        response = self.client.post(reverse('edit profile', kwargs={'pk': self.user_2.pk}), PROFILE_EDIT_DATA)
        self.assertEqual(404, response.status_code)


class AddProfileViewTests(TestCase):

    def setUp(self):
        self.user_1 = UserModel.objects.create_user(email=USER_1_DATA['email'])
        self.user_1.set_password(USER_1_DATA['password'])
        self.user_1.save()
        self.PHONE_CODE = CountryCodes.objects.create(name='BG', code='+359')

    def test_add_profile_success(self):
        PROFILE_ADD_DATA = {
            'first_name': 'Ivan',
            'middle_name': '',
            'last_name': 'Ivanov',
            'birth_date': date(1999, 2, 23),
            'gender': 'M',
            'phone_code': self.PHONE_CODE.pk,
            'phone': '999999999',
        }
        self.client.login(**USER_1_DATA)
        with self.assertRaises(exceptions.ObjectDoesNotExist):
            Profile.objects.get(user=self.user_1)
        response = self.client.post(reverse('create profile'), PROFILE_ADD_DATA)
        self.assertEqual(302, response.status_code)
        self.assertTrue(self.user_1.profile)
