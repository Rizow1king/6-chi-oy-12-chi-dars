from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate


def home(request: WSGIRequest):
    lessons = Lesson.objects.all()
    context = {
        "lessons": lessons,
        'title': 'Barcha kurs hamda darslar'
    }
    return render(request, "index.html", context)


def lessons_by_courses(request: WSGIRequest, course_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = Lesson.objects.filter(course_id=course_id)

    context = {
        'courses': [course],
        'lessons': lesson,
    }

    return render(request, 'index.html', context)


def lessons(request: WSGIRequest, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    context = {
        'lesson': lesson,
        'title': f'{lesson.name} - batafsil ma\'lumot'
    }
    return render(request, 'detail.html', context)


def course(request: WSGIRequest, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course = get_object_or_404(Course, id=lesson.course.id)
    course.views += 1
    course.save()
    context = {
        'lesson': lesson,
        'title': lesson.description
    }

    return render(request, 'detail.html', context)


def add_course(request: WSGIRequest):
    if request.method == 'POST':
        form = CourseForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.create()
            messages.success(request, "Kurs muvaffaqiyatli qo'shildi!")
            return redirect('home')
        else:
            messages.error(request, "Kurs qo'shishda xatolik yuz berdi.")
    else:
        form = CourseForm()

    context = {
        "form": form
    }
    return render(request, 'add_course.html', context)


def add_lesson(request: WSGIRequest):
    if request.method == 'POST':
        form = LessonForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            lesson = form.create()
            messages.success(request, "Dars muvaffaqiyatli tarzda qo'shildi!")
            return redirect('detail_lesson', lesson_id=lesson.pk)
        else:
            messages.error(request, "Dars qo'shishda xatolik yuz berdi.")
    else:
        form = LessonForm()

    context = {
        "form": form
    }
    return render(request, 'add_lesson.html', context)


def update_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, pk=lesson_id)
    if request.method == 'POST':
        form = LessonForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.update(lesson)
            messages.success(request, "Dars muvaffaqiyatli tarzda o'zgartirildi!")
            return redirect('lesson', lesson_id=lesson.pk)
        else:
            messages.error(request, "Darsni o'zgartirishda xatolik yuz berdi.")
    form = LessonForm(initial={
        'name': lesson.name,
        'teacher': lesson.teacher,
        'theme': lesson.theme,
        'homework': lesson.homework,
        'student_count': lesson.student_count,
        'published': lesson.published,
        'course': lesson.course,
        "photo": lesson.photo
    })
    context = {
        'form': form,
        'photo': lesson.photo,
        'lesson_id': lesson.pk,
        'lesson': lesson
    }
    return render(request, 'add_lesson.html', context)


def delete_lesson(request, lesson_id):
    lesson = Lesson.objects.get(pk=lesson_id)
    course_id = lesson.course.id
    if request.method == 'POST':
        lesson.delete()
        messages.success(request, "Dars muvaffaqiyatli tarzda o'chirildi!")
        return redirect('course', course_id=course_id)
    context = {
        'lesson': lesson
    }
    messages.warning(request, "Ushbu darsni o'chirmoqchimisiz?")
    return render(request, 'confirm_delete.html', context)


def register(request: WSGIRequest):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            password_confirm = form.cleaned_data.get('password_confirm')
            if password_confirm == password:
                user = User.objects.create_user(
                    form.cleaned_data.get("username"),
                    form.cleaned_data.get("email"),
                    password
                )
                messages.success(request, "Akkaunt muvaffaqiyatli qo'shildi!")
                return redirect('login')
            else:
                messages.error(request, "Parollar mos kelmaydi!")
    context = {
        "form": RegisterForm()
    }
    return render(request, "auth/register.html", context)


def login_view(request: WSGIRequest):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                messages.success(request, "Xush kelibsiz!!!")
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Login yoki parol noto'g'ri.")
    context = {
        "form": LoginForm()
    }
    return render(request, "auth/login.html", context)


def logout_view(request: WSGIRequest):
    logout(request)
    messages.success(request, "Siz muvaffaqiyatli tarzda chiqdingiz.")
    return redirect('login')


def terms(request: WSGIRequest):
    return render(request, "terms.html")


def comment_save(request: WSGIRequest, flower_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            lesson = get_object_or_404(Lesson, pk=flower_id)
            form = CommentForm(data=request.POST)
            if form.is_valid():
                comment = Comment.objects.create(
                    text=form.cleaned_data.get("text"),
                    author=request.user,
                    lesson=lesson
                )
                messages.success(request, "Izoh muvaffaqiyatli qo'shildi!")
            else:
                messages.error(request, "Izoh qo'shishda xatolik yuz berdi.")
        return redirect('flower_detail', flower_id=flower_id)
    messages.error(request, "Avval login qiling!!!")
    return redirect('login')


def comment_delete(request: WSGIRequest, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user == comment.author or request.user.is_superuser:
            lesson_id = comment.lesson.pk
            comment.delete()
            messages.success(request, "Izoh muvaffaqiyatli o'chirildi!")
            return redirect('lesson', lesson_id=lesson_id)
    messages.error(request, "Avval login qiling!!!")
    return redirect('login')


def comment_update(request: WSGIRequest, comment_id):
    comments = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        form = LessonForm(data=request.POST)
        if form.is_valid():
            flower_id = comments.flower.pk
            form.update(comments)
            messages.success(request, "Izoh muvaffaqiyatli o'zgartirildi!")
            return redirect('lesson', flower_id=flower_id)

    form = CommentForm(initial={
        'text': comments.text,
    })

    context = {
        'form': form
    }

    return render(request, 'detail.html', context)
