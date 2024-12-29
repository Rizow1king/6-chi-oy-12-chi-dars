from django.db import models
from django.contrib.auth.models import User


class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Nomi')
    definition = models.TextField(blank=True, null=True, verbose_name='Tavsiri')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Turi'
        verbose_name_plural = 'Turlari'
        ordering = ['-id']


class Flowers(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Nomi')
    description = models.TextField(default="Avtor ma'lumot qo'shmadi:)", verbose_name='Tavsifi')
    price = models.IntegerField(verbose_name='Narxi')
    quantity = models.IntegerField(verbose_name='Soni')
    published = models.BooleanField(default=False, verbose_name='Korinadimi',
                                    help_text='Agar bu yerda - "False" bolsa bu gul sotuvda korinmaydi, Agar "True" bolsa korinadi')
    type = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name='Turi')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Gul'
        verbose_name_plural = 'Gullar'
        ordering = ["-id"]


class Comment(models.Model):
    text = models.CharField(max_length=1200, verbose_name="Matni")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Kim qoldirgani")
    flower = models.ForeignKey(Flowers, on_delete=models.CASCADE, verbose_name="Ulangan guli")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Qo'shilgan vaqti")

    def __str__(self):
        return f"{self.author.username} | {self.text[:20]} | {self.flower.name[:20]}"

    class Meta:
        verbose_name = 'Izoh'
        verbose_name_plural = 'Izohlar'
        ordering = ['-created']