# Generated by Django 2.0.2 on 2020-06-15 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200615_0012'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slider',
            field=models.BooleanField(default=False),
        ),
    ]
