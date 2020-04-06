# Generated by Django 3.0.3 on 2020-03-27 08:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('solutions', '0006_auto_20200306_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('message', models.TextField()),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_comments', to='solutions.Comment')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_comments', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='sub_comment_likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]