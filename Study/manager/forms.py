from django import forms
from .models import *


class CourseForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'placeholder': 'kurs nomini kiriting!',
        'class': "form-control"

    }), label="Dars nomi")

    photo = forms.ImageField(widget=forms.FileInput(attrs={
        "class": 'form-control'
    }), label='Rasmi', required=False)

    def create(self):
        course = Course.objects.create(**self.cleaned_data)
        return course


class LessonForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "placeholder": "darsni nomini kiriting",
        "class": "form-control"
    }), label='Darsni nomi')
    teacher = forms.CharField(max_length=100, min_length=10, widget=forms.TextInput(attrs={
        "placeholder": "O'qituvchini ismini kiriting",
        "class": "form-control"
    }), label="O'qituvchini ismi")
    theme = forms.CharField(max_length=100, min_length=10, widget=forms.Textarea(attrs={
        "placeholder": "darsni mavzusini kiriting",
        "class": "form-control"
    }), label="Darsni mavzusi")
    homework = forms.CharField(max_length=100, min_length=10, widget=forms.Textarea(attrs={
        "placeholder": "uyga vazifani kiriting",
        "class": "form-control",
        "value": "Darsni qaytadan ko‘ring va o‘zingiz uchun konspekt qiling"
    }), label="Uyga vazifa")

    published = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': "form-check-input",
        'checked': 'checked'
    }), label='Saytda korinishi')
    course = forms.ModelChoiceField(queryset=Course.objects.all(), widget=forms.Select(attrs={
        'class': 'form-select'
    }), label="Bog'langan kursi")
    student_count = forms.IntegerField(widget=forms.NumberInput(attrs={
        'placeholder': "Talabalar sonini kiriting",
        'class': 'form-control'
    }), label='Talabalar soni')
    photo = forms.ImageField(widget=forms.FileInput(attrs={
        "class": 'form-control'
    }), label='Rasmi', required=False)

    def update(self, lesson):
        lesson.name = self.cleaned_data.get('name')
        lesson.teacher = self.cleaned_data.get('teacher')
        lesson.theme = self.cleaned_data.get('theme')
        lesson.photo = self.cleaned_data.get('photo') if self.cleaned_data.get('photo') else lesson.photo
        lesson.student_count = self.cleaned_data.get('student_count')
        lesson.published = self.cleaned_data.get('published')
        lesson.course = self.cleaned_data.get('course')
        lesson.homework = self.cleaned_data.get('homework')
        lesson.save()

    def create(self):
        lesson = Lesson.objects.create(**self.cleaned_data)
        return lesson


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'id': 'form3Example1cg',
        'class': 'form-control form-control-lg'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'id': 'form3Example3cg',
        'class': 'form-control form-control-lg'
    }))
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={
        'id': 'form3Example4cg',
        'class': 'form-control form-control-lg'
    }))
    password_confirm = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={
        'id': 'form3Example4cdg',
        'class': 'form-control form-control-lg'
    }))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        "class": 'form-control form-control-lg',
        "placeholder": 'Ismingizni kiriting'
    }), label='Ism:')

    password = forms.CharField(min_length=8, widget=forms.PasswordInput(attrs={
        "class": "form-control form-control-lg",
        "placeholder": "Parolingizni kirting:"
    }), label="Parol:")


class CommentForm(forms.Form):
    text = forms.CharField(
        max_length=1200,
        # validators=[validate_description],
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
        }),
        label="Izohingizni qoldiring:"
    )

    def update(self, comments):
        comments.text = self.cleaned_data.get('text')
        comments.save()
