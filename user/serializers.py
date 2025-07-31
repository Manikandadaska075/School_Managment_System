from rest_framework import serializers
from user.models import CustomUser, StudentProfile, TeacherProfile
from Academic.models import SubjectMarks,Department

class AdminRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'user_type']
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class TeacherProfileCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    address = serializers.CharField(write_only=True)
    department = serializers.CharField(write_only=True)
    position = serializers.CharField(write_only=True)
    subject = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password',
                  'address', 'department', 'position', 'subject']

    def create(self, validated_data):
        address = validated_data.pop('address')
        department = validated_data.pop('department')
        position = validated_data.pop('position')
        subject = validated_data.pop('subject')
        password = validated_data.pop('password')

        if not Department.objects.filter(department_name=department, subject=subject).exists():
            raise serializers.ValidationError(
                {"detail": f"The subject '{subject}' is not available in the department '{department}'."}
            )

        validated_data['user_type'] = 'teacher'
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()

        TeacherProfile.objects.create(
            teacher_id=user,
            address=address,
            department=department,
            position=position,
            subject=subject
        )
        return user

class TeacherProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='teacher_id.username')
    email = serializers.EmailField(source='teacher_id.email')
    user_type = serializers.CharField(source='teacher_id.user_type')
    class Meta:
        model = TeacherProfile
        fields = [ 'teacher_id', 'username', 'email', 'user_type','department', 'subject']

class StudentProfileCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    address = serializers.CharField(write_only=True)
    department = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'user_type',
                  'address', 'department']

    def create(self, validated_data):
        address = validated_data.pop('address')
        department_name = validated_data.pop('department')
        password = validated_data.pop('password')

        if not Department.objects.filter(department_name=department_name).exists():
            raise serializers.ValidationError({"detail": f"No department named '{department_name}' found."})

        validated_data['user_type'] = 'student'
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()

        StudentProfile.objects.create(
            Student_id=user,
            address=address,
            department=department_name
        )

        subjects = Department.objects.filter(department_name=department_name)

        for subject in subjects:
            SubjectMarks.objects.create(
                student_id=user,
                subject_code=subject,
                mark=0 
            )

        return user

class SubjectMarkSerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source='subject_code.subject_code')
    subject = serializers.CharField(source='subject_code.subject')

    class Meta:
        model = SubjectMarks
        fields = ['subject_code', 'subject', 'mark']
   
class StudentProfileSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='Student_id.id')
    username = serializers.CharField(source='Student_id.username')
    email = serializers.EmailField(source='Student_id.email')
    user_type = serializers.CharField(source='Student_id.user_type')
    subjects = serializers.SerializerMethodField()

    class Meta:
        model = StudentProfile
        fields = ['id', 'username', 'email', 'user_type', 'department', 'address', 'subjects']

    def get_subjects(self, obj):
        subject_marks = SubjectMarks.objects.filter(student_id=obj.Student_id)
        return SubjectMarkSerializer(subject_marks, many=True).data
