# Generated by Django 3.0.5 on 2020-04-05 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_social',
            field=models.BooleanField(default=False),
        ),
    ]
