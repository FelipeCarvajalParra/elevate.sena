# Generated by Django 5.0.3 on 2024-05-20 22:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mensaje',
            old_name='fecha',
            new_name='fech_mensa',
        ),
    ]