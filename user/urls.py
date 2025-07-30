from django.urls import path
from user import views

urlpatterns=[
    path('AdminRegistration/', views.AdminRegistration.as_view(), name='admin-register'),
    path('AdminLogin/', views.AdminLogin.as_view()),
    path('RegistrationByAdmin/',views.RegistrationByAdmin.as_view()),
    path('delete-userbyadmin/', views.DeleteUserByAdmin.as_view()),
    path('TeacherLogin/', views.TeacherLogin.as_view()),
    path('teacherprofileview/', views.TeacherProfileView.as_view()),
    path('Studentlogin/',views.StudentLogin.as_view()),
    path('studentprofileview/',views.StudentProfileView.as_view())
]