import json
from datetime import date, timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from api.models import CustomUser, Authority, Report, District, School
from api.serializers import AuthoritySerializer, FullReportSerializer, SchoolSerializer, ReportSerializer


class AuthorityTests(APITestCase):

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
        authority = Authority.objects.create(
            user=self.user, district=self.district)
        self.user.is_authority = True
        self.user.save()
        return authority

    def create_schools_reporting_to_authority(self, authority, num_schools):
        schools = []
        for i in range(num_schools):
            school_user = CustomUser.objects.create_user(
                username='schooluser{}'.format(i + 1),
                email='su{}@example.com'.format(i + 1),
                password='Tv#jlI2O*F'
            )
            school = School.objects.create(
                user=school_user,
                name='School {}'.format(i + 1),
                district=self.district,
                authority=authority
            )
            schools.append(school)
        return schools

    def create_reports_with_school(self, school, num_reports):
        reports = []
        for i in range(num_reports):
            report = Report.objects.create(
                school=school,
                reported_student_count=45,
                reported_for_date=(date.today() - timedelta(i)),
                reported_menu={},
                estimated_student_count=50,
                estimated_menu={}
            )
            reports.append(report)
        return reports

    def test_authority_enroll_with_auth(self):
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

    def test_authority_enroll_without_auth(self):
        url = reverse('authority_enroll')
        data = {"district": self.district.id}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Authority.objects.count(), 0)

    def test_authority_retrieve_with_auth(self):
        url = reverse('authority_me_retrieve_update')

        self.api_authenticate()
        authority = self.create_authority_with_current_user()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        authority_serializer_data = AuthoritySerializer(authority).data
        response_data = json.loads(response.content)
        self.assertEqual(response_data, authority_serializer_data)

    def test_authority_retrieve_without_auth(self):
        url = reverse('authority_me_retrieve_update')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authority_update_with_auth(self):
        url = reverse('authority_me_retrieve_update')

        self.api_authenticate()
        authority = self.create_authority_with_current_user()

        new_district = District.objects.create(name="ABC")
        data = {"district" : new_district.id}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        authority = Authority.objects.get(user_id=authority.user_id)
        authority_serializer_data = AuthoritySerializer(authority).data
        response_data = json.loads(response.content)
        self.assertEqual(response_data, authority_serializer_data)

    def test_authority_update_without_auth(self):
        url = reverse('authority_me_retrieve_update')

        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authority_report_list_with_auth(self):
        url = reverse('authority_report_list')

        self.api_authenticate()
        authority = self.create_authority_with_current_user()
        schools = self.create_schools_reporting_to_authority(authority, 2)
        all_reports = []
        for school in schools:
            all_reports.extend(self.create_reports_with_school(school, 2))

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        full_report_serializer_data = FullReportSerializer(
            all_reports, many=True).data
        response_data = json.loads(response.content)
        self.assertEqual(response_data, full_report_serializer_data)

    def test_authority_report_list_without_auth(self):
        url = reverse('authority_report_list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SchoolTests(APITestCase):

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

    def create_reports_by_school(self, school, num_reports):
        reports = []
        for i in range(num_reports):
            report = Report.objects.create(
                school=school,
                reported_student_count=45,
                reported_for_date=(date.today() - timedelta(i)),
                reported_menu={}
            )
            reports.append(report)
        return reports

    def create_school_with_current_user(self):
        school = School.objects.create(
            user=self.user,
            name='School A',
            district=self.district
        )
        return school

    def test_school_enroll_with_auth(self):
        url = reverse('school_enroll')
        data = {'name': 'School A', 'district': self.district.id}

        self.api_authenticate()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(School.objects.count(), 1)
        school = School.objects.get()
        self.assertEqual(school.name, 'School A')
        self.assertEqual(school.user, self.user)
        self.assertEqual(school.district, self.district)

    def test_school_enroll_without_auth(self):
        url = reverse('school_enroll')
        data = {'name': 'School A', 'district': self.district.id}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Authority.objects.count(), 0)

    def test_school_retrieve_with_auth(self):
        url = reverse('school_me_retrieve_update')

        self.api_authenticate()
        school = self.create_school_with_current_user()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        school_serializer_data = SchoolSerializer(school).data
        response_data = json.loads(response.content)
        self.assertEqual(response_data, school_serializer_data)

    def test_school_retrieve_without_auth(self):
        url = reverse('school_me_retrieve_update')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_school_update_with_auth(self):
        url = reverse('school_me_retrieve_update')

        self.api_authenticate()
        school = self.create_school_with_current_user()

        new_district = District.objects.create(name="ABC")
        data = {'name': 'School B', "district" : new_district.id}

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        school = School.objects.get(user_id=school.user_id)
        school_serializer_data = SchoolSerializer(school).data
        response_data = json.loads(response.content)
        self.assertEqual(response_data, school_serializer_data)

    def test_school_update_without_auth(self):
        url = reverse('school_me_retrieve_update')

        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_school_report_create_with_auth(self):
        url = reverse('school_report_list_create')
        data = {
            'reported_student_count': 45,
            'reported_menu': {
                'item1': '1',
                'item2': '2 servings'
            },
            'reported_for_date': '2020-01-10'
        }

        self.api_authenticate()
        school = self.create_school_with_current_user()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Report.objects.count(), 1)
        report = Report.objects.get()
        self.assertEqual(report.school, school)
        self.assertEqual(report.reported_student_count,
                         data['reported_student_count'])
        self.assertEqual(report.reported_menu, data['reported_menu'])
        self.assertEqual(report.reported_for_date, date(2020, 1, 10))

    def test_school_report_create_without_auth(self):
        url = reverse('school_report_list_create')
        data = {
            'reported_student_count': 45,
            'reported_menu': {
                'item1': '1',
                'item2': '2 servings'
            },
            'reported_for_date': '2020-01-10'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Report.objects.count(), 0)

    def test_school_report_list_with_auth(self):
        url = reverse('school_report_list_create')

        self.api_authenticate()
        school = self.create_school_with_current_user()
        reports = self.create_reports_by_school(school, 2)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        report_serializer_data = ReportSerializer(reports, many=True).data
        response_data = json.loads(response.content)
        self.assertEqual(response_data, report_serializer_data)

    def test_school_report_list_without_auth(self):
        url = reverse('school_report_list_create')

        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_school_report_retrieve_with_auth(self):
        self.api_authenticate()
        school = self.create_school_with_current_user()
        report = Report.objects.create(
                school=school,
                reported_student_count=45,
                reported_for_date=date.today(),
                reported_menu={}
            )

        url = reverse('school_report_retrieve_update', kwargs={"pk": report.pk})
 
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
   
        report_serializer_data = ReportSerializer(report).data
        response_data = json.loads(response.content)
        self.assertEqual(response_data, report_serializer_data)

    def test_school_report_retrieve_without_auth(self):
        self.api_authenticate()
        school = self.create_school_with_current_user()
        report = Report.objects.create(
                school=school,
                reported_student_count=45,
                reported_for_date=date.today(),
                reported_menu={}
            )
        
        url = reverse('school_report_retrieve_update', kwargs={"pk": report.pk})

        self.client.credentials() 

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_school_report_update_with_auth(self):
        self.api_authenticate()
        school = self.create_school_with_current_user()
        report = Report.objects.create(
                school=school,
                reported_student_count=45,
                reported_for_date=date.today(),
                reported_menu={}
            )
        
        data = {
            'reported_student_count': 40,
            'reported_for_date': '2020-01-10',
            'reported_menu': "vadapav"
        }

        url = reverse('school_report_retrieve_update', kwargs={"pk": report.pk})
 
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        report = Report.objects.get(id=report.id)
        report_serializer_data = ReportSerializer(report).data
        response_data = json.loads(response.content)
        self.assertEqual(response_data, report_serializer_data)

    def test_school_report_update_without_auth(self):
        self.api_authenticate()
        school = self.create_school_with_current_user()
        report = Report.objects.create(
                school=school,
                reported_student_count=45,
                reported_for_date=date.today(),
                reported_menu={}
            )
        
        url = reverse('school_report_retrieve_update', kwargs={"pk": report.pk})

        self.client.credentials()        

        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)