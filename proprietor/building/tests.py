from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse
from proprietor.building.models import Apartment, Building


UserModel = get_user_model()

USER_1_DATA = {"email": "m@m.com", "password": "admin123123"}

USER_2_DATA = {"email": "m2@m.com", "password": "admin123123"}

USER_3_DATA = {"email": "m3@m.com", "password": "admin123123"}

BUILDING_DATA = {
    "city": "Sofia",
    "street_address": "Any street",
    "block_number": "1",
    "postal_code": "1000",
    "floors_count": 6,
}

APARTMENT_1_DATA = {
    "floor": 1,
    "number": 1,
    "area": 64.5,
    "rooms_count": 2,
    "share": 8.23,
}

APARTMENT_2_DATA = {
    "floor": 1,
    "number": 2,
    "area": 64.5,
    "rooms_count": 2,
    "share": 8.23,
}


class MyApartmentsViewTest(TestCase):
    def setUp(self):
        self.user_1 = UserModel.objects.create_user(email=USER_1_DATA["email"])
        self.user_1.set_password(USER_1_DATA["password"])
        self.user_1.save()

        self.user_2 = UserModel.objects.create_user(email=USER_2_DATA["email"])
        self.user_2.set_password(USER_2_DATA["password"])
        self.user_2.save()

        self.user_3 = UserModel.objects.create_user(email=USER_3_DATA["email"])
        self.user_3.set_password(USER_3_DATA["password"])
        self.user_3.save()

        self.building = Building.objects.create(**BUILDING_DATA)
        self.building.save()

        APARTMENT_1_DATA.update({"building": self.building})
        self.apartment_1 = Apartment.objects.create(**APARTMENT_1_DATA)
        self.apartment_1.owner.add(self.user_1)
        self.apartment_1.save()

        APARTMENT_2_DATA.update({"building": self.building})
        self.apartment_2 = Apartment.objects.create(**APARTMENT_2_DATA)
        self.apartment_2.owner.add(self.user_2)
        self.apartment_2.save()

    def test_showing_only_my_apartments_success(self):
        self.client.login(**USER_1_DATA)
        response = self.client.get(reverse('my apartments'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response.context['apartment_list']))
        self.assertIn(self.apartment_1, response.context['apartment_list'])
        self.assertNotIn(self.apartment_2, response.context['apartment_list'])

    def test_user_with_no_apartments(self):
        self.client.login(**USER_3_DATA)
        response = self.client.get(reverse('my apartments'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response.context['apartment_list']))
 
    def test_not_logged_in_user_404(self):
        response = self.client.get(reverse('my apartments'))
        self.assertEqual(302, response.status_code)


class AddApartmentViewTest(TestCase):
    def setUp(self):
        self.user_1 = UserModel.objects.create_user(email=USER_1_DATA["email"])
        self.user_1.set_password(USER_1_DATA["password"])
        self.user_1.save()

        self.building = Building.objects.create(**BUILDING_DATA)
        self.building.save()

        APARTMENT_1_DATA.update({"building": self.building})
        self.apartment_1 = Apartment.objects.create(**APARTMENT_1_DATA)
        self.apartment_1.owner.add(self.user_1)
        self.apartment_1.save()

    def test_add_apartment_not_logged_in_user_403(self):
        response = self.client.get(reverse('create apartment', kwargs={'pk': self.building.pk}))
        self.assertEqual(403, response.status_code)

    def test_add_apartment_no_permission_403(self):
        self.building.manager = self.user_1
        self.building.save()
        self.client.login(**USER_1_DATA)
        response = self.client.get(reverse('create apartment', kwargs={'pk': self.building.pk}))
        self.assertEqual(403, response.status_code)

    def test_manager_add_apartment_with_permission_success(self):
        self.building.manager = self.user_1
        self.building.save()
        permission = Permission.objects.get(name='Can add apartment')
        self.user_1.user_permissions.add(permission)
        self.client.login(**USER_1_DATA)
        self.assertTrue(self.user_1.is_authenticated)
        self.assertTrue(self.user_1.has_perm('building.add_apartment'))
        response = self.client.get(reverse('create apartment', kwargs={'pk': self.building.pk}))
        self.assertEqual(200, response.status_code)

    def test_not_manager_add_apartment_with_permission_403(self):
        permission = Permission.objects.get(name='Can add apartment')
        self.user_1.user_permissions.add(permission)
        self.client.login(**USER_1_DATA)
        self.assertTrue(self.user_1.is_authenticated)
        self.assertTrue(self.user_1.has_perm('building.add_apartment'))
        response = self.client.get(reverse('create apartment', kwargs={'pk': self.building.pk}))
        self.assertEqual(403, response.status_code)
