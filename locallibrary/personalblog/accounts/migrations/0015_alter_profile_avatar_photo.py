# Generated by Django 3.2 on 2021-06-06 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_alter_profile_avatar_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar_photo',
            field=models.ImageField(default='static/main/assets/images/default_avatar.jpg', upload_to='profile_photo'),
        ),
    ]