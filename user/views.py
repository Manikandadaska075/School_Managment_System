from rest_framework.response import Response
from rest_framework.views import APIView
from user.serializers import AdminRegistrationSerializer, TeacherProfileCreateSerializer,TeacherProfileSerializer, StudentProfileCreateSerializer ,StudentProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from user.models import CustomUser, StudentProfile,TeacherProfile
from Academic.models import Department
from rest_framework.views import APIView
from rest_framework.response import Response
from user.permissions import IsCustomUser, IsStudent, IsTeacher
from rest_framework.permissions import IsAuthenticated, AllowAny

class AdminRegistration(APIView):
    def post(self, request):
        data = request.data
        data['user_type'] = 'admin'
        serializer = AdminRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Admin registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminLogin(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user and user.is_superuser: 
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials or not admin"}, status=status.HTTP_401_UNAUTHORIZED)

class RegistrationByAdmin(APIView):
    permission_classes = [IsAuthenticated, IsCustomUser]

    def post(self, request, *args, **kwargs):
        user_type = request.data.get("user_type")
        if not user_type:
            return Response({"error": "user_type is required"}, status=400)
        if user_type == "teacher":
            serializer = TeacherProfileCreateSerializer(data=request.data)
        elif user_type == "student":
            serializer = StudentProfileCreateSerializer(data=request.data)
        else:
            return Response({"error": "Invalid or missing user_type"}, status=400)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

class DeleteUserByAdmin(APIView):
    permission_classes = [IsAuthenticated, IsCustomUser]  # Adjust to [IsAdminUser] or your custom permission

    def delete(self, request):
        user_id = request.query_params.get('user_id')
        user_type = request.query_params.get('user_type')

        if not user_id or not user_type:
            return Response({"error": "Missing 'user_id' or 'user_type' in query parameters."}, status=400)

        try:
            user = CustomUser.objects.get(id=user_id, user_type=user_type)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        if user_type == "student":
            StudentProfile.objects.filter(Student_id=user).delete()

        elif user_type == "teacher":
            TeacherProfile.objects.filter(teacher_id=user).delete()
            Department.objects.filter(teacher_id=user).delete()

        elif user_type == "admin":
            return Response({"error": "Admin deletion not allowed."}, status=403)

        else:
            return Response({"error": "Invalid user_type."}, status=400)

        user.delete()
        return Response({"message": f"{user_type.capitalize()} and related records deleted successfully."})

class AdminUserListView(APIView):
    permission_classes = [IsAuthenticated, IsCustomUser]

    def get(self, request, user_type):
        if user_type == "teacher":
            teachers = TeacherProfile.objects.all()
            serializer = TeacherProfileSerializer(teachers, many=True)
        elif user_type == "student":
            students = StudentProfile.objects.all()
            serializer = StudentProfileSerializer(students, many=True)
        else:
            return Response({"error": "Invalid user_type"}, status=400)

        return Response(serializer.data, status=200)
    
class TeacherLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user and user.user_type == 'teacher':
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                })
        else:
            return Response({"error": "Invalid credentials or not a teacher"}, status=401)
        
class TeacherProfileView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]

    def get(self, request):
        try:
            profile = TeacherProfile.objects.get(teacher_id=request.user)
            serializer = TeacherProfileSerializer(profile)
            return Response(serializer.data)
        except TeacherProfile.DoesNotExist:
            return Response({"error": "Teacher profile not found"}, status=404)
        
class StudentLogin(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user and user.user_type == 'student':
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({"error": "Invalid credentials or not a student"}, status=401)
        
class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    def get(self, request):
        try:
            profile = StudentProfile.objects.get(Student_id=request.user)
            serializer = StudentProfileSerializer(profile)
            return Response(serializer.data)
        except StudentProfile.DoesNotExist:
            return Response({"error": "Student profile not found"}, status=404)