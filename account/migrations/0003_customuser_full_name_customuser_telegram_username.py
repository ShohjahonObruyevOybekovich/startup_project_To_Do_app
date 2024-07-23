# Generated by Django 5.0.4 on 2024-06-05 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_customuser_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='full_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='telegram_username',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
