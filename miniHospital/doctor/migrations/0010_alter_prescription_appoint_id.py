# Generated by Django 4.1 on 2023-03-16 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0018_alter_appointmentconfirmation_id'),
        ('doctor', '0009_alter_prescription_appoint_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescription',
            name='appoint_id',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patient.appointmentconfirmation'),
        ),
    ]