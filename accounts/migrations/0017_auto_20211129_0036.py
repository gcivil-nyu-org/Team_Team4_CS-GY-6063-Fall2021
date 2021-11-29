# Generated by Django 3.2.7 on 2021-11-29 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_review_review_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.TextField(blank=True, default='', max_length=256),
        ),
        migrations.AddField(
            model_name='profile',
            name='business_hours',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_text',
            field=models.TextField(blank=True, max_length=256),
        ),
    ]
