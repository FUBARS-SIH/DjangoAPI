from api.models import *
from datetime import date

district1 = District.objects.create(name="chennai") 
district2 = District.objects.create(name="trichy") 
district3 = District.objects.create(name="madurai") 
district4 = District.objects.create(name="salem") 
district5 = District.objects.create(name="theni") 

schedules = []

district=district1
items1 = ['idly', 'sidedish', 'rice', 'egg', 'chappati']
for day in range(5):
    schedules.append(Schedule.objects.create(district=district, day=day, item=items1[day]))

items2 = ['dosa', 'roti', 'dal', 'naan', 'bokra']
for day in range(5):
    schedules.append(Schedule.objects.create(district=district, day=day, item=items2[day]))

user1 = CustomUser.objects.create_user(username="auth", email="jyuvaraj000@gmail.com", password="teddybear", is_authority=True)
user2 = CustomUser.objects.create_user(username="school1", email="school1@gmail.com", password="leomessilm10")
user3 = CustomUser.objects.create_user(username="school2", email="school2@gmail.com", password="ronaldocr7")
user4 = CustomUser.objects.create_user(username="school3", email="school3@gmail.com", password="neymarjunior")

authority = Authority.objects.create(user=user1, district=district1)

school1 = School.objects.create(user=user2, name="SBOI" ,district=district1)
school2 = School.objects.create(user=user3, name="PSBB" ,district=district1)
school3 = School.objects.create(user=user4, name="DAV" ,district=district1)


report1 = Report.objects.create(school=school1, student_count=45, for_date=date(2020,8,3), added_by_school=True)
report2 = Report.objects.create(school=school2, student_count=45, for_date=date(2020,8,3), added_by_school=True)
report3 = Report.objects.create(school=school3, student_count=50, for_date=date(2020,8,3), added_by_school=True)


day = date(2020,8,3).weekday()
items = Schedule.objects.filter(district=district1, day=day)
for item in items:
    report1.items.create(item=item.item)
    report2.items.create(item=item.item)
    report3.items.create(item=item.item)


estimate_report1 = Report.objects.create(school=school1, student_count=45, for_date=date(2020,8,3), added_by_school=False, actual_report=report1)
estimate_report2 = Report.objects.create(school=school2, student_count=20, for_date=date(2020,8,3), added_by_school=False, actual_report=report2)
estimate_report3 = Report.objects.create(school=school3, student_count=45, for_date=date(2020,8,3), added_by_school=False, actual_report=report3)

for item in items:
    estimate_report1.items.create(item=item.item)
    estimate_report3.items.create(item=item.item)

