from django.urls import path
from .views import *

urlpatterns = [
    path('',home),
    path('logout/',logout_user, name= 'logout'),
    path('login/',login_user,name='login'),
    path('signup/',signup_user, name='signup'),
    path('requestcall/',requestcall, name='requestcall'),
    path('courses/',courses, name='courses'),
    path('profile/',profile,name='profile'),
    path('course_detail/<int:id>/',view_course,name='course_detail'),
    path('course/<int:id>/enroll/',enroll_course,name='enroll_course'),
    path('course/<int:id>/enrollment-success/',enrollment_success, name='enrollment_success'),
    path('my-course/',my_courses,name='my_courses')
    
]