from .views import *
from django.urls import path

urlpatterns = [
    path("", home, name="home"),
    path("courses/<int:course_id>/", lessons_by_courses, name='course'),
    path("lesson/<int:lesson_id>/", lessons, name='lesson'),
    path('course/add', add_course, name='add_course'),
    path('lesson/add', add_lesson, name='add_lesson'),
    path('lesson/<int:lesson_id>/update/', update_lesson, name='update_lesson'),
    path('lesson/<int:lesson_id>/delete/', delete_lesson, name='delete_lesson'),
    path('flower/<int:flower_id>/comment_save', comment_save, name='comment_save'),
    path('flower/<int:comment_id>/comment_delete', comment_delete, name='comment_delete'),
    path('flower/<int:comment_id>/comment_update', comment_update, name='comment_update'),
    path("register/", register, name="register"),
    path("register/terms", terms, name="terms"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]
