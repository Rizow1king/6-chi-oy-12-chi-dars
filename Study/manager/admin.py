from django.contrib import admin
from .models import *


class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", 'name', 'views', "created_at")
    list_display_links = ("id", "name")
    actions_on_top = False
    actions_on_bottom = True
    list_filter = ('name',)
    search_fields = ('name',)
    readonly_fields = ("views",)


class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "teacher", "theme", "published", "course")
    list_display_links = ("id", "name", "teacher")
    list_per_page = 5
    list_editable = ("theme",)
    list_filter = ("course", "published", "teacher")
    actions_on_top = False
    actions_on_bottom = True
    search_fields = ("description", "name", "teacher")


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'lesson', 'created')
    list_display_links = ('text', 'id')
    list_filter = ('lesson', 'author')
    search_fields = ('text', 'author', 'id')
    list_per_page = 10
    actions_on_bottom = True
    actions_on_top = False


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Comment, CommentAdmin)