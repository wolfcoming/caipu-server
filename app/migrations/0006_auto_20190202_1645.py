# Generated by Django 2.1.5 on 2019-02-02 08:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_greens_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menucategory',
            name='add_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='添加时间'),
        ),
    ]
