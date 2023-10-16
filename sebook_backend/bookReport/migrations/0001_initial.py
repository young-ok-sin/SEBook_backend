# Generated by Django 4.2.6 on 2023-10-14 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookReport',
            fields=[
                ('reportNum', models.AutoField(primary_key=True, serialize=False)),
                ('reportContents', models.TextField()),
                ('reportTitle', models.TextField()),
            ],
            options={
                'db_table': 'bookreport',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LikeBookReport',
            fields=[
                ('like_bookreportNum', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'like_bookreport',
                'managed': False,
            },
        ),
    ]
