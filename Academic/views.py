from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DepartmentSerializer,StudentDepartmentMarkDetailSerializer,StudentMarkDetailSerializer
from rest_framework.permissions import IsAuthenticated
from Academic.permissions import IsCustomUser,IsDepartmentTeacher,IsDepartmentHOD,IsStudent
from user.models import TeacherProfile,CustomUser,StudentProfile
from Academic.models import SubjectMarks,Department
from django.shortcuts import get_object_or_404

class CreateDepartment(APIView):
    permission_classes = [IsAuthenticated, IsCustomUser]

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Department created successfully', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentStudentListView(APIView):
    permission_classes = [IsAuthenticated, IsDepartmentTeacher]

    def get(self, request):
        user = request.user

        try:
            teacher_profile = TeacherProfile.objects.get(teacher_id=user)
            subject_name = teacher_profile.subject 

            department = get_object_or_404(Department, subject=subject_name)

            students = SubjectMarks.objects.filter(subject_code=department)

            serializer = StudentMarkDetailSerializer(students, many=True)
            return Response(serializer.data, status=200)

        except TeacherProfile.DoesNotExist:
            return Response({"error": "Teacher profile not found."}, status=404)
        
class DepartmentStudentListViewByHOD(APIView):
    permission_classes = [IsAuthenticated, IsDepartmentHOD]

    def get(self, request):
        user = request.user

        try:
            teacher_profile = TeacherProfile.objects.get(teacher_id=user)
            department_name = teacher_profile.department

            students = StudentProfile.objects.filter(department=department_name)

            serializer = StudentDepartmentMarkDetailSerializer(students, many=True)
            return Response(serializer.data, status=200)

        except TeacherProfile.DoesNotExist:
            return Response({"error": "Teacher profile not found."}, status=404)


class UpdateStudentMarksByTeacherOrAdmin(APIView):
    permission_classes = [IsAuthenticated, IsDepartmentTeacher]

    def put(self, request):
        user = request.user
        student_id = request.query_params.get("student_id")
        mark = request.query_params.get("mark")

        if not student_id or mark is None:
            return Response({"error": "Both 'student_id' and 'mark' are required in query parameters"}, status=400)

        try:
            mark = int(mark)
        except ValueError:
            return Response({"error": "Mark must be an integer"}, status=400)

        try:
            teacher_profile = TeacherProfile.objects.get(teacher_id=user)
        except TeacherProfile.DoesNotExist:
            return Response({"error": "Teacher profile not found"}, status=404)

        subject_name = teacher_profile.subject
        department = get_object_or_404(Department, subject=subject_name)

        try:
            student = CustomUser.objects.get(id=student_id, user_type='student')
        except CustomUser.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)

        try:
            subject_mark = SubjectMarks.objects.get(student_id=student, subject_code=department)
        except SubjectMarks.DoesNotExist:
            return Response({"error": "Marks entry not found for this student and subject"}, status=404)

        subject_mark.mark = mark
        subject_mark.save()

        return Response({
            "message": "Student mark updated successfully",
            "student": {
                "student_id": student.id,
                "subject": subject_mark.subject_code.subject,
                "mark": subject_mark.mark
            }
        }, status=status.HTTP_200_OK)


class StudentTotalMarksView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get_grade(self, mark):
        if mark >= 90:
            return "A+"
        elif mark >= 80:
            return "A"
        elif mark >= 70:
            return "B"
        elif mark >= 60:
            return "C"
        elif mark >= 50:
            return "D"
        elif mark >= 40:
            return "E"
        else:
            return "F"

    def get(self, request):
        user = request.user

        try:
            profile = StudentProfile.objects.get(Student_id=user)
        except StudentProfile.DoesNotExist:
            return Response({"error": "Student profile not found"}, status=404)

        subject_marks = SubjectMarks.objects.filter(student_id=user).select_related('subject_code')

        if not subject_marks.exists():
            return Response({"error": "No marks found for this student."}, status=404)

        total = 0
        subject_list = []
        failed_subjects = 0

        for entry in subject_marks:
            subject = entry.subject_code
            mark = entry.mark
            status = "Pass" if mark >= 40 else "Fail"
            if status == "Fail":
                failed_subjects += 1

            grade = self.get_grade(mark)

            subject_list.append({
                "subject_code": subject.subject_code,
                "subject": subject.subject,
                "mark": mark,
                "status": status,
                "grade": grade
            })

            total += mark

        count = subject_marks.count()
        percentage = round(total / count, 2) if count > 0 else 0
        overall_status = "Pass" if failed_subjects == 0 else "Fail"
        overall_grade = self.get_grade(percentage)

        return Response({
            "student_id": user.id,
            "username": user.username,
            "department": profile.department if isinstance(profile.department, str) else profile.department.department_name,
            "subjects": subject_list,
            "total_marks": total,
            "percentage": percentage,
            "overall_status": overall_status,
            "overall_grade": overall_grade
        }, status=200)

class TeacherSubjectMarksView(APIView):
    permission_classes = [IsAuthenticated, IsDepartmentTeacher]

    def get_grade(self, mark):
        if mark >= 90:
            return "A+"
        elif mark >= 80:
            return "A"
        elif mark >= 70:
            return "B"
        elif mark >= 60:
            return "C"
        elif mark >= 50:
            return "D"
        elif mark >= 40:
            return "E"
        else:
            return "F"

    def get(self, request):
        teacher = request.user

        try:
            profile = TeacherProfile.objects.get(teacher_id=teacher)
        except TeacherProfile.DoesNotExist:
            return Response({"error": "Teacher profile not found."}, status=404)

        subject_name = profile.subject

        try:
            department = Department.objects.get(subject=subject_name)
        except Department.DoesNotExist:
            return Response({"error": "Subject not found in department."}, status=404)

        marks_qs = SubjectMarks.objects.filter(subject_code=department).select_related('student_id')

        if not marks_qs.exists():
            return Response({"message": "No students found for this subject."})

        student_results = []
        for entry in marks_qs:
            mark = entry.mark
            status = "Pass" if mark >= 40 else "Fail"
            grade = self.get_grade(mark)

            student_results.append({
                "student_id": entry.student_id.id,
                "student_name": entry.student_id.username,
                "mark": mark,
                "grade": grade,
                "status": status
            })

        total_students = marks_qs.count()

        return Response({
            "teacher": teacher.username,
            "subject": subject_name,
            "department": department.department_name,
            "subject_code": department.subject_code,
            "total_students": total_students,
            "results": student_results
        })
    

class HODDepartmentStatsView(APIView):
    permission_classes = [IsAuthenticated, IsDepartmentHOD]

    def get(self, request):
        user = request.user

        try:
            profile = TeacherProfile.objects.get(teacher_id=user, position='HOD')
        except TeacherProfile.DoesNotExist:
            return Response({"error": "HOD profile not found."}, status=404)

        department_name = profile.department

        subjects = Department.objects.filter(department_name=department_name)
        if not subjects.exists():
            return Response({"error": "No subjects found in this department."}, status=404)

        result_data = []

        for subject in subjects:
            subject_marks = SubjectMarks.objects.filter(subject_code=subject)
            total = subject_marks.count()
            passed = subject_marks.filter(mark__gte=40).count()
            failed = total - passed

            result_data.append({
                "subject_code": subject.subject_code,
                "subject": subject.subject,
                "total_students": total,
                "passed": passed,
                "failed": failed,
                "pass_percentage": round((passed / total) * 100, 2) if total > 0 else 0,
            })

        return Response({
            "hod": user.username,
            "department": department_name,
            "subjects": result_data
        })
    