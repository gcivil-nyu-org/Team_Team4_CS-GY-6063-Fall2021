# Generated by Django 3.2.8 on 2021-10-25 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20211024_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date_posted',
            field=models.DateTimeField(default='%2021-%10-%25 %13:%Oct'),
        ),
    ]
