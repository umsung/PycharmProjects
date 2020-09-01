# Generated by Django 2.2 on 2020-06-24 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('restfulapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('song', models.CharField(default='', max_length=100)),
                ('singer', models.CharField(default='', max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'music',
            },
        ),
    ]
