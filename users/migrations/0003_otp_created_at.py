# Generated by Django 4.2 on 2024-01-03 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_otp_expirydate'),
    ]

    operations = [
        migrations.AddField(
            model_name='otp',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
