from django.urls import path
from Academic import views

urlpatterns = [
    path('DepartmentStudentList/',views.DepartmentStudentListView.as_view()),
    path('StudentlistviewByHOD/',views.DepartmentStudentListViewByHOD.as_view()),
    path('CreateDepartmentByAdmin/', views.CreateDepartment.as_view()),
    path('UpdateStudentMarksByTeacherOrAdmin/', views.UpdateStudentMarksByTeacherOrAdmin.as_view()),
    path('teacher-subject-marks/', views.TeacherSubjectMarksView.as_view()),
    path('department-stats/', views.HODDepartmentStatsView.as_view()),
    path('student-total-marks/', views.StudentTotalMarksView.as_view()),
]