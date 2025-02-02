import json
from datetime import date, timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from api.models import CustomUser, Authority, Report, District, School, ReportItem, Schedule
from api.serializers import AuthoritySerializer, SchoolSerializer, SchoolReportSerializer, SchoolReportCreateSerializer, DistrictSerializer, AuthorityReportSerializer, EstimateReportSerializer
import datetime 
import calendar 

class AuthorityTests(APITestCase):

    def setUp(self):
        self.district = District.objects.create(name='XYZ')

        self.user = CustomUser.objects.create_user(
            username='user1',
            email='user1@gmail.com',
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
                email='su{}@gmail.com'.format(i + 1),
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

    def create_actual_report_with_school_for_date(self, school, date):
        report = Report.objects.create(
            school=school,
            student_count=45,
            for_date=date,
            added_by_school=True
        )
        items = ['idly', 'dosa', 'chutney']
        report.items.bulk_create(
            [ReportItem(report=report, item=item) for item in items])
        return report

    def create_estimate_report_for_actual_report(self, actual_report):
        report = Report.objects.create(
            school=actual_report.school,
            student_count=45,
            for_date=actual_report.for_date,
            actual_report=actual_report
        )
        items = ['idly', 'dosa']
        report.items.bulk_create(
            [ReportItem(report=report, item=item) for item in items])
        return report

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
        data = {"district": new_district.id}

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

    def test_authority_report_list_without_auth(self):
        url = reverse('authority_report_list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SchoolTests(APITestCase):

    def setUp(self):
        self.district = District.objects.create(name='XYZ')
        self.user = CustomUser.objects.create_user(
            username='user1',
            email='user1@gmail.com',
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
                student_count=45,
                for_date=(date.today() - timedelta(i)),
                added_by_school=True
            )
            items = ['idly', 'dosa']
            report.items.bulk_create(
                [ReportItem(report=report, item=item) for item in items])
            reports.append(report)
        return reports

    def create_school_with_current_user(self):
        school = School.objects.create(
            user=self.user,
            name='School A',
            district=self.district
        )
        return school


    def create_schedule(self):
        district=self.district
        items = ['idly', 'dosa', 'vada', 'egg', 'chappati']
        for day in range(5):
            Schedule.objects.create(
                district=district, 
                day=day, 
                item=items[day]
            )


    def findDay(self,date): 
        days = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4}
        date = datetime.datetime.strptime(date, '%Y-%m-%d').weekday() 
        day_str = calendar.day_name[date]
        day_int = days[day_str]
        return (day_int) 


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
        data = {'name': 'School B', "district": new_district.id}

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
        url = reverse('school_report_create')
        data = {
            'student_count': 45,
            'for_date': '2020-01-10',
        }

        day = self.findDay(data['for_date'])
        district = self.district
        self.api_authenticate()
        school = self.create_school_with_current_user()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Report.objects.count(), 1)
        report = Report.objects.get()
        self.assertEqual(report.school, school)
        self.assertEqual(report.student_count,
                         data['student_count'])
        self.assertEqual(report.for_date, date(2020, 1, 10))

    def test_school_report_create_without_auth(self):
        url = reverse('school_report_create')
        data = {
            'student_count': 45,
            'for_date': '2020-01-10',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Report.objects.count(), 0)

    def test_school_report_list_with_auth(self):
        url = reverse('school_report_list')

        self.api_authenticate()
        school = self.create_school_with_current_user()
        reports = self.create_reports_by_school(school, 2)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        report_serializer_data = SchoolReportSerializer(
            reports, many=True).data
        response_data = json.loads(response.content)
        self.assertCountEqual(response_data, report_serializer_data)

    def test_school_report_list_without_auth(self):
        url = reverse('school_report_list')

        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_school_report_retrieve_with_auth(self):
        self.api_authenticate()
        school = self.create_school_with_current_user()
        report = Report.objects.create(
            school=school,
            student_count=45,
            for_date=(date.today()),
            added_by_school=True
        )
        items = ['idly', 'dosa', 'chutney']
        report.items.bulk_create(
            [ReportItem(report=report, item=item) for item in items])
        
        url = reverse('school_report_retrieve',
                      kwargs={"pk": report.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        report_serializer_data = SchoolReportSerializer(report).data
        response_data = json.loads(response.content)
        self.assertEqual(response_data, report_serializer_data)

    def test_school_report_retrieve_without_auth(self):
        self.api_authenticate()
        school = self.create_school_with_current_user()
        report = Report.objects.create(
            school=school,
            student_count=45,
            for_date=(date.today()),
        )
        items = ['idly', 'dosa', 'chutney']
        report.items.bulk_create(
            [ReportItem(report=report, item=item) for item in items])

        url = reverse('school_report_retrieve',
                      kwargs={"pk": report.pk})

        self.client.credentials()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DistrictTests(APITestCase):

    def setUp(self):
        self.districts = []
        for i in range(3):
            self.districts.append(District.objects.create(
                name='District{}'.format(i + 1)))

    def test_district_list(self):
        url = reverse('district_list')

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        district_serializer_data = DistrictSerializer(
            self.districts, many=True).data
        response_data = json.loads(response.content)
        self.assertEqual(response_data, district_serializer_data)


class EstimateReportTests(APITestCase):

    def setUp(self):
        self.district = District.objects.create(name='XYZ')
        self.user = CustomUser.objects.create_user(username='xxx', email='f@gmail.com', password='xxxxxxx')
        self.school = School.objects.create(user=self.user, name='AAA', district=self.district)
    
    def create_estimated_report(self):
        report = Report.objects.create(
            school=self.school,
            student_count=45,
            for_date= '2020-01-10',
        )
        items = ['idly', 'dosa']
        report.items.bulk_create(
            [ReportItem(report=report, item=item) for item in items])
        return report

    def test_estimate_report_create(self):
        url = reverse('estimate_report_list_create')
        school = self.school
        data = {
            'student_count': 45,
            'for_date': '2020-01-10',
            'items': [
                {'item': 'idly'},
                {'item': 'dosa'}
            ],
            'school': school.user.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Report.objects.count(), 1)
        report = Report.objects.get()
        self.assertEqual(report.student_count,
                         data['student_count'])
        self.assertEqual(report.items.count(), len(data['items']))
        test_items_list = list(map((lambda d: d['item']), data['items']))
        for i, item in enumerate(report.items.all()):
            self.assertEqual(item.report.id, report.id)
            self.assertTrue(item.item in test_items_list)
        self.assertEqual(report.for_date, date(2020, 1, 10))

    def test_estimate_report_retrieve(self):
        school = self.school
        report = Report.objects.create(
            school=school,
            student_count=45,
            for_date=(date.today()),
        )
        items = ['idly', 'dosa', 'chutney']
        report.items.bulk_create(
            [ReportItem(report=report, item=item) for item in items])

        url = reverse('estimate_report_retrieve_update',
                      kwargs={"pk": report.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        report_serializer_data = EstimateReportSerializer(report).data
        response_data = json.loads(response.content)
        self.assertEqual(response_data, report_serializer_data)
