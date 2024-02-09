# Generated by Django 4.1.5 on 2023-11-03 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taasapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultOfStudents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricno', models.CharField(max_length=50)),
                ('semester', models.IntegerField()),
                ('department', models.IntegerField()),
                ('faculty', models.IntegerField()),
                ('level', models.IntegerField()),
                ('score', models.IntegerField()),
                ('coursecode', models.CharField(max_length=20)),
                ('point', models.FloatField()),
                ('grade', models.CharField(max_length=5)),
                ('createdBy', models.CharField(max_length=100)),
                ('userID', models.CharField(max_length=100)),
                ('sessionID', models.IntegerField()),
                ('createdAt', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]