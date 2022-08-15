# Generated by Django 3.2.9 on 2022-08-15 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_applicationmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationmodel',
            name='demurrage',
        ),
        migrations.RemoveField(
            model_name='applicationmodel',
            name='demurrage_dolla',
        ),
        migrations.RemoveField(
            model_name='applicationmodel',
            name='mobile_area_code',
        ),
        migrations.RemoveField(
            model_name='applicationmodel',
            name='phone_area_code',
        ),
        migrations.AlterField(
            model_name='applicationmodel',
            name='biz_zip_code',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]