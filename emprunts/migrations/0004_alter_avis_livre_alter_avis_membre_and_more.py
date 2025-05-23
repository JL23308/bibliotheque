# Generated by Django 5.2 on 2025-04-25 10:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emprunts', '0003_alter_emprunt_livre_alter_emprunt_membre'),
        ('livres', '0009_remove_emprunt_livre_remove_emprunt_membre_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='avis',
            name='livre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='livres.livre'),
        ),
        migrations.AlterField(
            model_name='avis',
            name='membre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emprunts.membre'),
        ),
        migrations.AlterField(
            model_name='membre',
            name='adresse',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='membre',
            name='telephone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='membre',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
