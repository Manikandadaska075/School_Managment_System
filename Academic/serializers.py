from rest_framework import serializers
from .models import Department,SubjectMarks
from user.models import StudentProfile

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['subject_code', 'department_name', 'subject']

class StudentMarkDetailSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(source='student_id.id')
    username = serializers.CharField(source='student_id.username')
    subject_code = serializers.CharField(source='subject_code.subject_code')
    subject = serializers.CharField(source='subject_code.subject')

    class Meta:
        model = SubjectMarks
        fields = ['student_id', 'username', 'subject_code', 'subject', 'mark']

class SubjectMarkSerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source='subject_code.subject_code')
    subject = serializers.CharField(source='subject_code.subject')

    class Meta:
        model = SubjectMarks
        fields = ['subject_code', 'subject', 'mark']


class StudentDepartmentMarkDetailSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='Student_id.id')
    username = serializers.CharField(source='Student_id.username')
    marks = serializers.SerializerMethodField()

    class Meta:
        model = StudentProfile
        fields = ['id', 'username', 'department', 'address', 'marks']

    def get_marks(self, obj):
        marks = SubjectMarks.objects.filter(student_id=obj.Student_id)
        return SubjectMarkSerializer(marks, many=True).data
    