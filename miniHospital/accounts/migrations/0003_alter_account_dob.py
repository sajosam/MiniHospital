# Generated by Django 4.1 on 2022-09-21 14:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_account_contact_account_district_account_dob_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='dob',
            field=models.DateField(default=datetime.date(2022, 9, 21)),
        ),
    ]
