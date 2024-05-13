# Generated by Django 3.1.1 on 2024-05-09 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BillingAdress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('mobile_number', models.CharField(max_length=11)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=11)),
                ('state', models.CharField(max_length=11)),
                ('zipcode', models.CharField(max_length=11)),
                ('country', models.CharField(max_length=11)),
            ],
        ),
    ]
