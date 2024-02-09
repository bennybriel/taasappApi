# Generated by Django 4.2.7 on 2023-12-03 19:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taasapp', '0002_resultofstudents'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taasapp.module')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('permissions', models.ManyToManyField(to='taasapp.permission')),
            ],
        ),
        migrations.CreateModel(
            name='StudentTranscript',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricno', models.CharField(max_length=50)),
                ('semesterID', models.IntegerField()),
                ('departmentID', models.IntegerField()),
                ('levelID', models.IntegerField()),
                ('score', models.IntegerField()),
                ('coursecode', models.CharField(max_length=20)),
                ('point', models.FloatField()),
                ('grade', models.CharField(max_length=5)),
                ('semester', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('level', models.CharField(max_length=100)),
                ('academicsession', models.CharField(max_length=100)),
                ('createdBy', models.CharField(max_length=100)),
                ('userID', models.CharField(max_length=100)),
                ('sessionID', models.IntegerField()),
                ('createdAt', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RenameField(
            model_name='resultofstudents',
            old_name='department',
            new_name='departmentID',
        ),
        migrations.RenameField(
            model_name='resultofstudents',
            old_name='faculty',
            new_name='levelID',
        ),
        migrations.RenameField(
            model_name='resultofstudents',
            old_name='level',
            new_name='semesterID',
        ),
        migrations.RenameField(
            model_name='studentrecords',
            old_name='department',
            new_name='countryID',
        ),
        migrations.RenameField(
            model_name='studentrecords',
            old_name='faculty',
            new_name='departmentID',
        ),
        migrations.RenameField(
            model_name='studentrecords',
            old_name='nationality',
            new_name='facultyID',
        ),
        migrations.RenameField(
            model_name='studentrecords',
            old_name='state',
            new_name='stateID',
        ),
        migrations.RemoveField(
            model_name='country',
            name='countryID',
        ),
        migrations.RemoveField(
            model_name='courier',
            name='courierID',
        ),
        migrations.RemoveField(
            model_name='department',
            name='departmentID',
        ),
        migrations.RemoveField(
            model_name='faculty',
            name='facultyID',
        ),
        migrations.RemoveField(
            model_name='level',
            name='levelID',
        ),
        migrations.RemoveField(
            model_name='lga',
            name='lgaID',
        ),
        migrations.RemoveField(
            model_name='programme',
            name='programmeID',
        ),
        migrations.RemoveField(
            model_name='resultofstudents',
            name='semester',
        ),
        migrations.RemoveField(
            model_name='roletypes',
            name='roleID',
        ),
        migrations.RemoveField(
            model_name='semester',
            name='semesterID',
        ),
        migrations.RemoveField(
            model_name='session',
            name='sessionID',
        ),
        migrations.RemoveField(
            model_name='state',
            name='stateID',
        ),
        migrations.AddField(
            model_name='courses',
            name='semesterID',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='programme',
            name='department',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='schoolsettings',
            name='state',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='state',
            name='country',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='studentrecords',
            name='country',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users',
            name='apikey',
            field=models.CharField(default=1, max_length=200, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users',
            name='isapikey',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='courses',
            name='semester',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='department',
            name='facultyID',
            field=models.IntegerField(verbose_name=10),
        ),
        migrations.AlterField(
            model_name='programme',
            name='departmentID',
            field=models.IntegerField(verbose_name=10),
        ),
        migrations.AlterField(
            model_name='programme',
            name='facultyID',
            field=models.IntegerField(verbose_name=10),
        ),
        migrations.AlterField(
            model_name='schoolsettings',
            name='country',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='UserRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='taasapp.role')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]