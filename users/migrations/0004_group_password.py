# Generated by Django 3.0.3 on 2020-03-03 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200301_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='password',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
