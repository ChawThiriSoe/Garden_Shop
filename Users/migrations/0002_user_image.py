# Generated by Django 3.2.8 on 2021-10-08 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.FileField(null=True, upload_to='../images/'),
        ),
    ]
