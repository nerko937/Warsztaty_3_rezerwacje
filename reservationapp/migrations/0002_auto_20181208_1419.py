# Generated by Django 2.1.4 on 2018-12-08 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservationapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='projector',
            field=models.BooleanField(null=True, verbose_name='projektor'),
        ),
    ]