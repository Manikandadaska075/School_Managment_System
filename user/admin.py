from django.contrib import admin
from user.models import StudentProfile,TeacherProfile,CustomUser
from Academic.models import Department,SubjectMarks

admin.site.register(CustomUser)
admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
admin.site.register(Department)
admin.site.register(SubjectMarks)