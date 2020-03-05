# Generated by Django 3.0.3 on 2020-03-03 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('problems', '0003_auto_20200302_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.TextField()),
                ('lang', models.CharField(choices=[('c', 'c'), ('cpp', 'cpp'), ('java', 'java'), ('python', 'python'), ('javascript', 'javascript')], max_length=255)),
                ('caption', models.TextField(blank=True, null=True)),
                ('view', models.IntegerField(default=0)),
                ('solved', models.BooleanField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to=settings.AUTH_USER_MODEL)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solutions', to='problems.OriginProb')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('message', models.TextField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='solutions.Solution')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]