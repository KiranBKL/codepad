# Generated by Django 3.0.4 on 2020-06-28 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('practice', '0002_onlineide'),
    ]

    operations = [
        migrations.CreateModel(
            name='Input1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_program1', models.TextField()),
            ],
        ),
    ]
