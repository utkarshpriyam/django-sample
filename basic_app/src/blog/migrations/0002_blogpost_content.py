# Generated by Django 4.2.5 on 2023-10-03 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
