# Generated by Django 5.1.4 on 2024-12-20 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='student_count',
            field=models.IntegerField(default=10, verbose_name="O'quvchilar soni"),
        ),
    ]
