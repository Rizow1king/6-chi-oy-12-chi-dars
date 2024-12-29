from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nomi')
    photo = models.ImageField(upload_to="course", verbose_name='Rasmi', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Qoshilgan vaqti')
    views = models.IntegerField(verbose_name="ko'rilgan soni", default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kurs'
        verbose_name_plural = 'Kurslar'
        ordering = ['-id']


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='Darsni nomi')
    teacher = models.CharField(max_length=100, verbose_name="O'qituvchi ismi")
    theme = models.TextField(default="Darsni mavzusi: qo'shilmagan", blank=True, null=True,
                             verbose_name='Darsni mavzusi')
    homework = models.TextField(default='Darsni qatatdan korish va ozingiz uchun konspekt qiling',
                                verbose_name='Uyga vazifa')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")
    published = models.BooleanField(default=True, verbose_name='Bolganligi')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Qaysi kursga boglangani')
    student_count = models.IntegerField(verbose_name="O'quvchilar soni", default=10)
    photo = models.ImageField(upload_to='lessons.photos', verbose_name='Rasmi', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Dars'
        verbose_name_plural = 'Darslar'
        ordering = ["-id"]


class Comment(models.Model):
    text = models.CharField(max_length=1200, verbose_name="Matni")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Kim qoldirgani")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Ulangan guli")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")

    def __str__(self):
        return f"{self.author.username} | {self.text[:20]} | {self.lesson.name[:20]}"

    class Meta:
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'
        ordering = ['-created']
