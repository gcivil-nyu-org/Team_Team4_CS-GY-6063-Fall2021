# Generated by Django 3.2.8 on 2021-10-24 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_review_wifi_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='wifi_rating',
            field=models.IntegerField(),
        ),
    ]