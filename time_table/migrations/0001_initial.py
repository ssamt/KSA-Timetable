# Generated by Django 3.1.4 on 2020-12-27 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelData',
            fields=[
                ('lecture_data', models.TextField(max_length=750)),
                ('links', models.CharField(max_length=100)),
                ('is_valid', models.BooleanField(default=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='RawData',
            fields=[
                ('data', models.TextField(max_length=2000)),
                ('is_valid', models.BooleanField(default=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]