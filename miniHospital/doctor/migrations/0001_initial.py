# Generated by Django 4.1 on 2022-09-17 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Designation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('des_name', models.CharField(choices=[('General', 'General'), ('Consultant', 'Consultant'), ('Assistant', 'Assistant'), ('Junior', 'Junior'), ('Senior', 'Senior'), ('Professor', 'Professor'), ('practitioner', 'practitioner'), ('Senior practitioner', 'Senior practitioner'), ('Senior consultant', 'Senior consultant'), ('General Surgeon', 'General Surgeon'), ('Rectal Surgeon', 'Rectal Surgeon'), ('Neuro Surgeon', 'Neuro Surgeon'), ('orthopedic Surgeon', 'orthopedic Surgeon'), ('Pediatric Surgeon', 'Pediatric Surgeon'), ('Plastic Surgeon', 'Plastic Surgeon'), ('HOD', 'HOD'), ('Nurse', 'Nurse'), ('Physiotherapist', 'Physiotherapist'), ('Head Nurse', 'Head Nurse'), ('Lab Technician', 'Lab Technician'), ('Lab Assistant', 'Lab Assistant'), ('Lab Manager', 'Lab Manager'), ('Lab Director', 'Lab Director')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('spec_name', models.CharField(choices=[('Cardiology', 'Cardiology'), ('Neurology', 'Neurology'), ('Orthopedics', 'Orthopedics'), ('Gastroenterology', 'Gastroenterology'), ('Dermatology', 'Dermatology'), ('Psychiatry', 'Psychiatry'), ('Nephrology', 'Nephrology'), ('Urology', 'Urology'), ('Oncology', 'Oncology'), ('Radiology', 'Radiology'), ('Anesthesiology', 'Anesthesiology'), ('Dentistry', 'Dentistry'), ('Endocrinology', 'Endocrinology'), ('Gynaecology', 'Gynaecology'), ('Ophthalmology', 'Ophthalmology'), ('Paediatrics', 'Paediatrics'), ('Otolaryngology', 'Otolaryngology'), ('Rheumatology', 'Rheumatology'), ('Dermatology', 'Dermatology'), ('Pulmonology', 'Pulmonology'), ('Plastic Surgery', 'Plastic Surgery'), ('Physician', 'Physician'), ('Physiotherapy', 'Physiotherapy'), ('Psychologist', 'Psychologist'), ('Surgeon', 'Surgeon'), ('ENT', 'ENT'), ('Orthopedics', 'Orthopedics')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('year_of_service', models.IntegerField()),
                ('qual_name', multiselectfield.db.fields.MultiSelectField(choices=[('BDS', 'BDS'), ('BHMS', 'BHMS'), ('BPT', 'BPT'), ('B.Pharm', 'B.Pharm'), ('BUMS', 'BUMS'), ('MD', 'MD'), ('BYNS', 'BYNS'), ('DS', 'DS'), ('DCM', 'DCM'), ('DPM', 'DPM'), ('D.Pharm', 'D.Pharm'), ('MCM', 'MCM'), ('MMSc', 'MMSc'), ('MPH', 'MPH'), ('MM', 'MM'), ('M.Pharm', 'M.Pharm'), ('M.B.B.S', 'M.B.B.S'), ('M.Phy', 'M.Phy'), ('M.phil', 'M.phil'), ('Msc', 'Msc'), ('MS', 'MS'), ('DNB', 'DNB'), ('M.Ch', 'M.Ch')], max_length=100)),
                ('license_no', models.CharField(blank=True, max_length=100)),
                ('is_doctor', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_lab', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('des_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='des_name_doctor', to='doctor.designation')),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('spec_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spec_name_related', to='doctor.specialization')),
            ],
        ),
    ]
