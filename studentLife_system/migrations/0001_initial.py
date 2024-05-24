# Generated by Django 5.0.6 on 2024-05-17 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='studentInfo',
            fields=[
                ('studID', models.IntegerField(primary_key=True, serialize=False)),
                ('lrn', models.CharField(max_length=12)),
                ('lastname', models.CharField(max_length=100)),
                ('firstname', models.CharField(max_length=100)),
                ('middlename', models.CharField(max_length=50)),
                ('degree', models.CharField(max_length=150)),
                ('yearlvl', models.CharField(max_length=10)),
                ('sex', models.CharField(max_length=10)),
                ('emailadd', models.EmailField(max_length=254)),
                ('contact', models.CharField(max_length=11)),
            ],
            options={
                'ordering': ['lastname'],
            },
        ),
    ]
