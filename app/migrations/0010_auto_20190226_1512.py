# Generated by Django 2.1.5 on 2019-02-26 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20190225_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='greens',
            name='burden',
            field=models.CharField(default='', help_text='用料', max_length=10000, verbose_name='用料'),
        ),
        migrations.AlterField(
            model_name='greens',
            name='makes',
            field=models.CharField(default='', help_text='步骤', max_length=10000, verbose_name='步骤'),
        ),
    ]
