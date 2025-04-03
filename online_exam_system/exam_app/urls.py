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
    path('categories/add/', views.CategoryCreateView.as_view(), name='add_categories'),

    # Exam URLs
    path('exam/add/', views.ExamCreateView.as_view(), name='add_exam'),
    path('exam/<int:exam_id>/questions/add/', views.add_questions, name='add_questions'),
    path('exam/questions/add/', views.add_questions, name='add_questions_latest'),
    path('exam/<int:exam_id>/take/', views.take_exam, name='take_exam'),
    path('exam/history/', views.exam_history, name='exam_history'),

]
