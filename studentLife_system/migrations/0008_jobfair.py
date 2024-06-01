# Generated by Django 5.0.3 on 2024-06-01 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studentLife_system', '0007_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobFair',
            fields=[
                ('jobfair_id', models.AutoField(primary_key=True, serialize=False)),
                ('jobtitle', models.CharField(default='', max_length=255)),
                ('companyname', models.CharField(max_length=255)),
                ('joblocation', models.CharField(max_length=255)),
                ('employmenttype', models.CharField(max_length=100)),
                ('jobdescription', models.TextField()),
                ('jobsalary', models.CharField(max_length=255)),
            ],
        ),
    ]
