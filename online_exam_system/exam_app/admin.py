from django.contrib import admin
from .models import Category, Exam, Question, Choice, ExamAttempt, UserAnswer

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('text', 'exam', 'marks')
    list_filter = ('exam',)
    search_fields = ('text',)

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    show_change_link = True

class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_by', 'created_at', 'is_active')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]

class UserAnswerInline(admin.TabularInline):
    model = UserAnswer
    extra = 0
    readonly_fields = ('question', 'selected_choice', 'is_correct')

class ExamAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'started_at', 'completed_at', 'score')
    list_filter = ('exam', 'user', 'completed_at')
    search_fields = ('user__username', 'exam__title')
    inlines = [UserAnswerInline]
    readonly_fields = ('user', 'exam', 'started_at', 'completed_at', 'score')

admin.site.register(Category)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(ExamAttempt, ExamAttemptAdmin)
