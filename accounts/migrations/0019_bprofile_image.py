# Generated by Django 3.2.7 on 2021-11-29 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20211129_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='bprofile',
            name='image',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]