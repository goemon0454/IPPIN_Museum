# Generated by Django 3.1 on 2020-08-31 11:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0004_auto_20200831_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='update_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
