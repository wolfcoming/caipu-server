# Generated by Django 2.1.5 on 2019-02-25 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_menucategory_islast_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menucategory',
            name='islast_level',
            field=models.IntegerField(default=0, help_text='是否是最后级别', verbose_name='是否是最后级别'),
        ),
    ]