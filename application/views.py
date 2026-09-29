from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import *


def home(request):
    return render(request, 'home.html')


def requestcall(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        enquiry = request.POST.get('enquiry')
        message = request.POST.get('message')

        CallRequest.objects.create(
            name=name,
            email=email,
            phone=phone,
            enquiry=enquiry,
            message=message
        )

    return redirect('/')


@login_required
def profile(request):
    profile_, created = Profile.objects.get_or_create(user=request.user)

    return render(request, 'profile.html', {'profile': profile_})


@login_required
def profile_update(request):
    profile_, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')

        profile_.phone = request.POST.get('phone')
        profile_.bio = request.POST.get('bio')
        profile_.place = request.POST.get('place')

        if request.FILES.get('image'):
            profile_.image = request.FILES.get('image')

        request.user.save()
        profile_.save()

        messages.success(request, "Profile Updated Successfully")

        return redirect('profile')

    return redirect('profile')


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)

            request.session['student_id'] = user.id
            request.session['student_name'] = user.first_name
            request.session['student_email'] = user.email

            request.session.set_expiry(3600)

            messages.success(request, 'Login Successfully')

            response = redirect('/')

            response.set_cookie(
                'student_name',
                user.first_name,
                max_age=3600,
                httponly=True,
                samesite='Lax'
            )

            return response

        else:
            messages.error(request, 'Invalid Username or Password')

            return redirect('login')

    return render(request, 'login.html')


def signup_user(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already Registered')

            return redirect('signup')

        if Profile.objects.filter(phone=phone).exists():
            messages.error(request, 'The Phone Number Already Register')

            return redirect('signup')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=email,
            email=email,
            password=password
        )

        Profile.objects.create(
            user=user,
            phone=phone
        )

        messages.success(request, 'Sign Up successfully...')

        return redirect('login')

    return render(request, 'signup.html')


def logout_user(request):
    logout(request)
    response = redirect('login')
    response.delete_cookie('student_name')
    return response


def courses(request):
    data = Course.objects.all()
    return render(request, 'courses.html', {'courses': data })


def view_course(request, id):
    course = get_object_or_404(Course, id=id)
    modules = Module.objects.filter(course=course)
    return render(request, 'course_detail.html', {'course': course, 'modules': modules})


@login_required
def enroll_course(request, id):
    course = get_object_or_404(Course, id=id)

    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.info( request,"You're already enrolled in the course")

        return redirect('courses')

    if request.method == 'POST':
        goal = request.POST.get('goal')

        Enrollment.objects.create(
            student=request.user,
            course=course,
            goal=goal
            )

        messages.success( request,'Courses Successfully Enrolled')
        return redirect( 'enrollment_success',id=course.id )

    return render(request, 'enroll_course.html', {'course': course })


@login_required
def enrollment_success(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, 'enrollment_success.html', {'course': course})


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter( student=request.user).select_related('course')
    return render(request, 'my_courses.html', {'enrollments': enrollments})