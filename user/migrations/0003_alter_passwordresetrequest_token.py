# Generated by Django 5.2.1 on 2025-05-11 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_passwordresetrequest_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passwordresetrequest',
            name='token',
            field=models.CharField(default='4JnSHvJx9nPvP5zNQUPmU6vkfAIlIXRQ', editable=False, max_length=32, unique=True),
        ),
    ]
