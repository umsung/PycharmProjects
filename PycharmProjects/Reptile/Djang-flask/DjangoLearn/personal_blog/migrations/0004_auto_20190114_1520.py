# Generated by Django 2.1.4 on 2019-01-14 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_blog', '0003_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='blog/'),
        ),
    ]
