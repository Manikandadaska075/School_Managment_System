from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Cast
from django.db.models import IntegerField,Max

def generate_teacher_id():
    last_id = CustomUser.objects.filter(id__startswith='TS').aggregate(max_id=models.Max("id"))["max_id"]
    if last_id:
        num = int(last_id.replace("TS", "")) + 1
    else:
        num = 100
    return f"TS{num}"

def generate_student_id():
    last_id = CustomUser.objects.filter(id__regex=r'^\d{6,}$').aggregate(max_id=models.Max(Cast('id', IntegerField())))["max_id"]
    if last_id:
        num = last_id + 1
    else:
        num = 100000
    return num

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )

    user_type = models.CharField(max_length=10, choices = USER_TYPE_CHOICES)
    id = models.CharField(primary_key=True, editable=False)
    recorded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    def save(self, *args, **kwargs):
        if not self.id:
            if self.user_type == 'admin':
                self.is_superuser = True
                self.is_staff = True
                max_id = CustomUser.objects.filter(id__regex=r'^\d+$').aggregate(max_val=Max(Cast('id', IntegerField())))['max_val']
                self.id = str((max_id or 0) + 1)
            elif self.user_type == 'teacher':
                self.is_staff = True
                self.id = generate_teacher_id()
            else:
                self.is_staff = False
                self.id = generate_student_id()
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.user_type})"

class TeacherProfile(models.Model):
    POSITION_CHOICES = [
        ('HOD', 'Head of Department'),
        ('Teacher', 'Teacher'),
    ]
    teacher_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'teacher'},to_field='id')
    address = models.TextField()
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES)
    subject = models.CharField(max_length=100)
    recorded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.teacher_id}"

class StudentProfile(models.Model):
    Student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'},to_field='id')
    address = models.TextField()
    department = models.CharField(max_length=100)
    recorded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.Student_id}"