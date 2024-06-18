from django.contrib import admin

from materials.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Админка для модели Course
    """
    list_display = ('id', 'name', 'image', 'description')
    list_filter = ('name',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Админка для модели Lesson
    """
    list_display = ('id', 'name', 'description',)
    list_filter = ('name',)
