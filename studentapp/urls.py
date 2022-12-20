from django.urls import path
from . import views

urlpatterns = [
    path("", views.register , name="register"),
    path("login", views.login, name="login"),
    path("dashboard/<str:pk>/", views.dashboard, name='dashboard'),
    path("all-student", views.all_student, name="all-student"),
    path("student-details/<int:pk>", views.student_details, name='student-details')
]