# Generated by Django 3.2.7 on 2021-11-27 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_merge_20211124_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_text',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]