# Generated by Django 4.1 on 2023-03-18 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0045_alter_otp_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x00000176EB30B310>', max_length=200, unique=True),
        ),
    ]
