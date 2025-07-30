from django.db import models
from user.models import CustomUser

class Department(models.Model):
    subject_code = models.CharField(primary_key=True)
    department_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    recorded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"{self.department_name} - {self.subject}"
    
class SubjectMarks(models.Model):
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field='id')
    subject_code = models.ForeignKey(Department, on_delete=models.CASCADE, to_field='subject_code')
    mark = models.IntegerField()
    recorded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

