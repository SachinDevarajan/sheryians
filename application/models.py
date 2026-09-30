from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CallRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    enquiry = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'CallRequest'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profiles/',blank=True, null= True)
    bio = models.TextField(blank=True, default='')
    date_of_birth = models.DateField(null=True,blank=True)
    city = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, blank=True, default='' )
    pincode = models.CharField(max_length=10, blank=True, default='')
    country = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.user.username
    class Meta:
        db_table = 'Profile'


class Mentor(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='mentors/')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'mentor' 


class Course(models.Model):
    course_name = models.CharField(max_length=100)
    description = models.TextField()
    original_price = models.IntegerField()
    price = models.IntegerField()
    image = models.ImageField( upload_to='courses/', blank=True, null=True )
    mentor = models.ForeignKey( Mentor, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')

    tag1 = models.CharField( max_length=50, blank=True, default='' )
    tag2 = models.CharField( max_length=50, blank=True, default='' )
    tag3 = models.CharField( max_length=50, blank=True, default='')

    def __str__(self):
        return self.course_name

    class Meta:
        db_table = 'course'


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    name = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.course.course_name} - {self.name}'

    class Meta:
        db_table = 'module'
        ordering = ['order']


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('enrolled', 'Enrolled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    student = models.ForeignKey(User,on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    start_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField( max_length=20, choices=STATUS_CHOICES, default='enrolled' )
    progress = models.PositiveIntegerField( default=0)
    goal = models.TextField(blank=True, null=True)

    completed_at = models.DateTimeField(null=True, blank=True )

    class Meta:
        constraints = [ models.UniqueConstraint(
                            fields=["student", "course"],
                            name="unique_student_course"
                        )]
        db_table = 'enrollment'

    def __str__(self):
        return f'{self.student.username} - {self.course.course_name}'


class Lesson(models.Model):
    module = models.ForeignKey( Module, on_delete=models.CASCADE, related_name='lessons' )
    title = models.CharField( max_length=150 )
    description = models.TextField(blank=True, default='' )
    video_url = models.URLField( blank=True )
    duration = models.CharField( max_length=30, blank=True, default='' )
    order = models.PositiveIntegerField(default=1 )
    is_preview = models.BooleanField( default=False)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'lesson'
        ordering = ['order']

class LessonProgress(models.Model):
    student = models.ForeignKey( User, on_delete=models.CASCADE, related_name='lesson_progress' )
    lesson = models.ForeignKey( Lesson, on_delete=models.CASCADE, related_name='progress')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True )
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'lesson'],
                name='unique_student_lesson'
            )]
        db_table = 'lesson_progress'

    def __str__(self):
        return f'{self.student.username} - {self.lesson.title}'

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey( Course, on_delete=models.CASCADE, related_name='payments')
    amount = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending' )
    transaction_id = models.CharField( max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.username} - {self.course.course_name} - {self.status}'
    class Meta:
        db_table = 'payment'