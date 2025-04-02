from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.db import transaction
from django.forms import formset_factory

from .models import Category, Exam, Question, Choice, ExamAttempt, UserAnswer
from .forms import UserRegisterForm, CategoryForm, ExamForm, QuestionForm, ChoiceFormSet

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
        else:
            form = UserRegisterForm()
        return render(request, 'registration/register.html', {'form': form})
    
@login_required
def index(request):
    exams = Exam.objects.filter(is_active=True)
    categories = Category.objects.all()
    context = {
        'exams': exams,
        'categories': categories,
    }
    return render(request, 'exam_app/index.html', context)

# Category Views
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'exam_app/exam_categories.html'
    context_object_name = 'categories'

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'exam_app/add_category.html'
    success_url = reverse_lazy('categories')

# Exam Views
class ExamCreateView(LoginRequiredMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = 'exam_app/add_exam.html'
    success_url = reverse_lazy('add_questions')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
@login_required
def add_questions(request, exam_id=None):
    if exam_id:
        exam = get_object_or_404(Exam, id=exam_id)
    else:
        exam = Exam.objects.filter(created_by=request.user).latest('created_at')

    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.exam = exam
            question.save()

            choice_formset = ChoiceFormSet(request.POST, instance=question)
            if choice_formset.is_valid():
                choice_formset.save()
                messages.success(request, "Question added successfully!")

                # Check if user wants to add another question or finish
                if 'add_another' in request.POST:
                    return redirect('add_questions', exam_id=exam.id)
                else:
                    return redirect('index')
    else:
        question_form = QuestionForm()
        choice_formset = ChoiceFormSet()

    context = {
        'exam': exam,
        'question_form': question_form,
        'choice_formset': choice_formset,
    }
    return render(request, 'exam_app/add_questions.html', context)

@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)

    # Check if the user has already completed this exam
    previous_attempts = ExamAttempt.objects.filter(
        user=request.user,
        exam=exam,
        completed_at__isnull=False
    )

    if previous_attempts.exists():
        messages.info(request, "You have already completed this exam. You can view your results in the exam history.")
        return redirect('exam_history')
    
    # Check for an ongoing attempt
    ongoing_attempt = ExamAttempt.objects.filter(
        user=request.user,
        exam=exam,
        completed_at__isnull=True
    ).first()

    if not ongoing_attempt:
        # Create a new attempt
        ongoing_attempt = ExamAttempt.objects.create(
            user=request.user,
            exam=exam
        )

    questions = exam.get_questions()

    if request.method == 'POST':
        # Calculate score
        score = 0
        total_marks = exam.get_total_marks()

        for question in questions:
            selected_choice_id = request.POST.get(f'question_{question.id}')

            if selected_choice_id:
                selected_choice = Choice.objects.get(id=selected_choice_id)

                # Save user's answer
                UserAnswer.objects.create(
                    attempt=ongoing_attempt,
                    question=question,
                    selected_choice=selected_choice
                )

                # Update score if correct
                if selected_choice.is_correct:
                    score += question.marks

        # Calculate percentage score
        if total_marks > 0:
            percentage_score = (score / total_marks) * 100
        else:
            percentage_score = 0

        # Mark attempt as completed
        ongoing_attempt.completed_at = timezone.now()
        ongoing_attempt.score = percentage_score
        ongoing_attempt.save()

        messages.success(request, f"Exam submitted successfully! Your score: {percentage_score:.2f}%")
        return redirect('exam_history')
    
    context = {
        'exam': exam,
        'questions': questions,
        'attempt': ongoing_attempt,
    }
    return render(request, 'exam_app/take_exam.html', context)

@login_required
def exam_history(request):
    attempts = ExamAttempt.objects.filter(user=request.user).order_by('-started_at')
    context = {
        'attempts': attempts
    }
    return render(request, 'exam_app/exam_history.html', context)