# Generated by Django 5.2.1 on 2025-05-09 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Catégorie')),
                ('status', models.CharField(choices=[('Activée', 'Activée'), ('Désactivée', 'Désactivée')], default='Activée', max_length=10, verbose_name='Status')),
                ('img', models.ImageField(blank=True, null=True, upload_to='categories/', verbose_name='Image')),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='Date de creation')),
            ],
        ),
    ]
