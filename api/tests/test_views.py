import json
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from api.models import CustomUser, Authority, Report, District, School
from api.serializers import AuthoritySerializer

class AuthorityTests(APITestCase):

    @classmethod
    def setUp(self):
        self.district = District.objects.create(name='XYZ')

        self.user = CustomUser.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='Ltye$4T5'
        )

        self.token = Token.objects.create(user=self.user)

    def api_authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def create_authority_with_current_user(self):
        self.authority = Authority.objects.create(user=self.user, district=self.district)
        self.user.is_authority = True
        self.user.save()

    def test_authority_enroll_with_authentication(self):
        url = reverse('authority_enroll')
        data = {"district": self.district.id}

        self.api_authenticate()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Authority.objects.count(), 1)
        authority = Authority.objects.get()
        self.assertEqual(authority.user, self.user)
        self.assertEqual(authority.district.id, self.district.id)
        self.assertEqual(authority.district.name, self.district.name)

    def test_authority_enroll_without_authentication(self):
        url = reverse('authority_enroll')
        data = {"district": self.district.id}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Authority.objects.count(), 0)

    def test_authority_retrieve_with_authentication(self):
        url = reverse('authority_me_retrieve_update')

        self.api_authenticate()
        self.create_authority_with_current_user()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        authority_serializer_data = AuthoritySerializer(instance=self.authority).data
        response_data = json.loads(response.content)
        self.assertEqual(response_data, authority_serializer_data)

    def test_authority_retrieve_without_authentication(self):
        url = reverse('authority_me_retrieve_update')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authority_retrieve_update_with_authencation(self):
        pass

    def test_authority_retrieve_update_without_authencation(self):
        pass

    def test_authority_report_list_with_authentication(self):
        pass

    def test_authority_report_list_without_authentication(self):
        pass
