# Generated by Django 3.2.8 on 2021-10-25 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_review_date_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='wifi_rating',
            field=models.IntegerField(default=0),
        ),
    ]