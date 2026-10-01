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

    enrollments = Enrollment.objects.filter(student = request.user)
    enroll_count = enrollments.count()
    completed_count = enrollments.filter(status='completed').count()

    return render(request, 'profile.html', {'profile': profile_,'enrolled_count':enroll_count,'completed_count':completed_count})


@login_required
def edit_profile(request):
    profile_, created = Profile.objects.get_or_create( user=request.user)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        date_of_birth = request.POST.get('date_of_birth')
        bio = request.POST.get('bio')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        country = request.POST.get('country')

        request.user.first_name = first_name
        request.user.last_name = last_name

        profile_.phone = phone or ''
        profile_.date_of_birth = date_of_birth or None
        profile_.bio = bio or ''
        profile_.city = city or ''
        profile_.state = state or ''
        profile_.pincode = pincode or ''
        profile_.country = country or ''

        if request.FILES.get('image'):
            profile_.image = request.FILES.get('image')

        request.user.save()
        profile_.save()

        messages.success( request, 'Profile Updated Successfully' )
        return redirect('profile')

    return render(request, 'edit_profile.html',{ 'profile': profile_ })


@login_required
def profile_courses(request):
    profile_, created = Profile.objects.get_or_create( user=request.user)
    enrollments = Enrollment.objects.filter( student=request.user).select_related( 'course' ).order_by('-start_at' )
    enrolled_count = enrollments.count()
    completed_count = enrollments.filter(status='completed').count()

    context = {
                'profile': profile_,
                'enrollments': enrollments,
                'enrolled_count': enrolled_count,
                'completed_count': completed_count
            }

    return render(request, 'profile_courses.html',context )


@login_required
def profile_update(request):
    profile_, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')

        profile_.phone = request.POST.get('phone')
        profile_.bio = request.POST.get('bio')
        profile_.date_of_birth = request.POST.get('date_of_birth') or None
        profile_.city = request.POST.get('city')
        profile_.state = request.POST.get('state')
        profile_.pincode = request.POST.get('pincode')
        profile_.country = request.POST.get('country')

        if request.FILES.get('image'):
            profile_.image = request.FILES.get('image')

        request.user.save()
        profile_.save()

        messages.success(request, "Profile Updated Successfully")

        return redirect('profile')

    return redirect('profile')


@login_required
def profile_courses(request):
    profile_, created = Profile.objects.get_or_create(user=request.user)
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course').order_by('-start_at')
    enrolled_count = enrollments.count()
    completed_count = enrollments.filter(status='completed').count()

    context = {
                'profile': profile_,
                'enrollments': enrollments,
                'enrolled_count': enrolled_count,
                'completed_count': completed_count
            }
    
    return render(request, 'profile_courses.html',context)


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
    modules = course.modules.prefetch_related('lessons').all()
    return render(request, 'course_detail.html', {'course': course, 'modules': modules})


@login_required
def enroll_course(request, id):
    course = get_object_or_404(Course, id=id)

    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.info( request,"You're already enrolled in the course")

        return redirect('my_courses')

    if request.method == 'POST':
        goal = request.POST.get('goal')

        request.session['enrollment_course_id'] = course.id
        request.session['enrollment_goal'] = goal

        return redirect('payment',id=course.id)

    return render(request, 'enroll_course.html', {'course': course })


@login_required
def enrollment_success(request, id):
    course = get_object_or_404(Course, id=id)

    enrollment = get_object_or_404(Enrollment, student = request.user, course=course)

    return render(request, 'enrollment_success.html', {'course': course,'enrollment':enrollment})


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course').order_by('-start_at')

    return render(request, 'my_courses.html', {'enrollments': enrollments})

@login_required
def payment(request, id):
    course = get_object_or_404(Course, id=id)

    return render(request, 'payment.html', {
        'course': course
    })


@login_required
def process_payment(request, id):
    course = get_object_or_404(Course, id=id)

    if request.method == 'POST':
        goal = request.session.get('enrollment_goal', '')

        Payment.objects.create(
            student=request.user,
            course=course,
            amount=course.price,
            status='success'
        )

        enrollment, created = Enrollment.objects.get_or_create(
            student=request.user,
            course=course,
            defaults={
                'goal': goal,
                'status': 'enrolled',
                'progress': 0
            }
        )

        request.session.pop('enrollment_course_id', None)
        request.session.pop('enrollment_goal', None)

        messages.success(request, 'Payment Successful. Course Enrolled Successfully.')

        return redirect('enrollment_success', id=course.id)

    return redirect('payment', id=course.id)

@login_required
def learn_course(request, id):
    course = get_object_or_404(Course, id=id)

    enrollment = get_object_or_404(
        Enrollment,
        student=request.user,
        course=course
    )

    modules = course.modules.prefetch_related('lessons').all()

    context = {
        'course': course,
        'enrollment': enrollment,
        'modules': modules
    }

    return render(request, 'learn_course.html', context )