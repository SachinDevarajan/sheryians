from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Course)
admin.site.register(Mentor)
admin.site.register(Module)
admin.site.register(CallRequest)
admin.site.register(Profile)
admin.site.register(Enrollment)
admin.site.register(Lesson)
admin.site.register(Payment)