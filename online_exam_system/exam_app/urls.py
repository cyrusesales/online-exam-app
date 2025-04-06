from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='add_category'),

    # Exam URLs
    path('exams/add/', views.ExamCreateView.as_view(), name='add_exam'),
    path('exams/<int:exam_id>/questions/add/', views.add_questions, name='add_questions'),
    path('exams/questions/add/', views.add_questions, name='add_questions_latest'),
    path('exams/<int:exam_id>/take/', views.take_exam, name='take_exam'),
    path('exams/history/', views.exam_history, name='exam_history'),

]
