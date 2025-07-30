from rest_framework.permissions import BasePermission
from user.models import TeacherProfile
# from Academic.models import Department

class IsCustomUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_superuser
    
class IsDepartmentTeacher(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or user.user_type != 'teacher':
            return False
        try:
            teacher_profile = TeacherProfile.objects.get(teacher_id=user)
            return teacher_profile.department and teacher_profile.position in ['teacher', 'HOD']
        except TeacherProfile.DoesNotExist:
            return False

class IsDepartmentHOD(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated or user.user_type != 'teacher':
            return False
        try:
            teacher_profile = TeacherProfile.objects.get(teacher_id=user)
            return teacher_profile.department and teacher_profile.position == "HOD"
        except TeacherProfile.DoesNotExist:
            return False
        
class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'teacher'

class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'student'