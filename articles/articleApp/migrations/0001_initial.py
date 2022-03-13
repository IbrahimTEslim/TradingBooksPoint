# Generated by Django 4.0.2 on 2022-03-07 14:10

import articleApp.validators
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('rule', models.IntegerField(choices=[(1, 'Admin'), (2, 'Normal Client')], default=2)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('password', models.CharField(max_length=100)),
                ('university_id', models.CharField(max_length=10, unique=True, validators=[articleApp.validators.validate_university_id])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('author_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Facultie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectCode',
            fields=[
                ('subject_id', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('is_universirty_requirement', models.BooleanField(default=False)),
                ('semester', models.IntegerField(choices=[(1, 'First Semester'), (2, 'Seconod Semester')])),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='articleApp.department')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('amount', models.IntegerField(default=1)),
                ('op_code', models.IntegerField(choices=[(1, 'Donate'), (2, 'GiveBack'), (3, 'Borrow'), (4, 'Reserved')])),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='articleApp.book')),
                ('confirmed_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='admins', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cleint', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='facultie',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='articleApp.facultie'),
        ),
        migrations.AddField(
            model_name='book',
            name='subject_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='articleApp.subjectcode'),
        ),
    ]
