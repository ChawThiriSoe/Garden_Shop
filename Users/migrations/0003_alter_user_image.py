# Generated by Django 3.2.8 on 2021-10-09 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0002_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='static/images/default-image.png', null=True, upload_to='static/images/'),
        ),
    ]