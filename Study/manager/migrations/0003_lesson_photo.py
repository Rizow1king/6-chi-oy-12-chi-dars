# Generated by Django 5.1.4 on 2024-12-22 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_lesson_student_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='lessons.photos', verbose_name='Rasmi'),
        ),
    ]
