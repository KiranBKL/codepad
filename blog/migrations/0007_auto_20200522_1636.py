# Generated by Django 3.0.4 on 2020-05-22 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200520_2330'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='answer',
            new_name='reply',
        ),
    ]
