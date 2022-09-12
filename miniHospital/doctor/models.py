from django.db import models
from cloudinary.models import CloudinaryField
from datetime import date
from accounts.models import Account
from django import forms
from multiselectfield import MultiSelectField
# Create your models here.


class Specialization(models.Model):
    specialization_name=(
        ('Cardiology','Cardiology'),
        ('Neurology','Neurology'),
        ('Orthopedics','Orthopedics'),
        ('Gastroenterology','Gastroenterology'),
        ('Dermatology','Dermatology'),
        ('Psychiatry','Psychiatry'),
        ('Nephrology','Nephrology'),
        ('Urology','Urology'),
        ('Oncology','Oncology'),
        ('Radiology','Radiology'),
        ('Anesthesiology','Anesthesiology'),
        ('Dentistry','Dentistry'),
        ('Endocrinology','Endocrinology'),
        ('Gynaecology','Gynaecology'),
        ('Ophthalmology','Ophthalmology'),
        ('Paediatrics','Paediatrics'),
        ('Otolaryngology','Otolaryngology'),
        ('Rheumatology','Rheumatology'),
        ('Dermatology','Dermatology'),
        ('Pulmonology','Pulmonology'),
        ('Plastic Surgery','Plastic Surgery'),
        ('Physician','Physician'),
        ('Physiotherapy','Physiotherapy'),
        ('Psychologist','Psychologist'),
        ('Surgeon','Surgeon'),
        ('ENT','ENT'),
        ('Orthopedics','Orthopedics'),


    )

    id = models.AutoField(primary_key=True)
    spec_name = models.CharField(max_length=100, choices=specialization_name)

    def __str__(self):
        return self.spec_name

class Designation(models.Model):
    designation_names=(
        ('General','General'), #Doctor
        ('Consultant','Consultant'), #Consultant
        ('Assistant','Assistant'), #Assistant
        ('Junior','Junior'), #Junior
        ('Senior','Senior'), #Senior
        ('Professor','Professor'), #Professor
        ('practitioner','practitioner'), #practitioner
        ('Senior practitioner','Senior practitioner'), #Senior practitioner
        ('Senior consultant','Senior consultant'), #Senior consultant
        ('General Surgeon','General Surgeon'), #General Surgeon
        ('Rectal Surgeon','Rectal Surgeon'), #Rectal Surgeon
        ('Neuro Surgeon','Neuro Surgeon'), #Neuro Surgeon
        ('orthopedic Surgeon','orthopedic Surgeon'), #orthopedic Surgeon
        ('Pediatric Surgeon','Pediatric Surgeon'), #Pediatric Surgeon
        ('Plastic Surgeon','Plastic Surgeon'), #Plastic Surgeon
        ('HOD','HOD'), #HOD
        
        # for nurses
        ('Nurse','Nurse'), #Nurse
        ('Physiotherapist','Physiotherapist'), #Physiotherapist
        ('Head Nurse','Head Nurse'), #Head Nurse


        # for laboratory
        ('Lab Technician','Lab Technician'), #Lab Technician
        ('Lab Assistant','Lab Assistant'), #Lab Assistant
        ('Lab Manager','Lab Manager'), #Lab Manager
        ('Lab Director','Lab Director'), #Lab Director

    )

    id = models.AutoField(primary_key=True)
    des_name = models.CharField(max_length=100, choices=designation_names)

    def __str__(self):
        return self.des_name

# class Qualification(models.Model):
#     qualification_names=(
#         #doctors
#         ('BDS','BDS'),  #Bachelor of Dental Surgery
#         ('BHMS','BHMS'), #Bachelor of Homeopathy Medicine and Surgery
#         ('BPT','BPT'), #Bachelor of physiotherapy
#         ('B.Pharm','B.Pharm'), #bachelor of pharma
#         ('BUMS','BUMS'),  #Bachelor of Unani Medicine and Surgery
#         ('MD','MD'), #doctor of medicine
#         ('BYNS','BYNS'), #Bachelor of Yoga and Naturopathy Sciences
#         ('DS','DS'), #doctor of surgery
#         ('DCM','DCM'), #doctor of clinical medicine
#         ('DPM','DPM'), #doctor of public medicine
#         ('D.Pharm','D.Pharm'), #doctor of pharma
#         ('MCM','MCM'), #master of clinical medicine
#         ('MMSc','MMSc'), #master of medical science
#         ('MPH','MPH'), #master of public health
#         ('MM','MM'), #master of medicine
#         ('M.Pharm','M.Pharm'), #master of pharma
#         ('M.B.B.S','M.B.B.S'), #master of botany and botanical science
#         ('M.Phy','M.Phy'), #master of physiotherapy
#         ('M.phil','M.phil'), #master of philosophy
#         ('Msc','Msc'), #master of science
#         ('MS','MS'),  #master of surgery
#         ('DNB','DNB'), #Diplomate of National Board
#         ('M.Ch','M.Ch'), #Master of Chirurgiae

#         #For nurses
#         ('PN','PN'), #1. Diploma in Practical Nursing
#         ('ASN','ASN'), #2. Associate in Nursing
#         ('BSN','BSN'), #3. Bachelor of Nursing
#         ('MSN','MSN'), #4. Master of Nursing
#         ('DSN','DSN'), #5. Doctor of Nursing
#         ('B.Sc(N)','B.Sc(N)'), #8. Bachelor of Science in Nursing
#         ('M.Sc(N)','M.Sc(N)'), #9. Master of Science in Nursing
#         ('BDN','BDN'), #10. Bachelor of Dental Nursing
#         ('CNA','CNA'), #11. Certificate in Nursing Administration

#         # for laboratory
#         ('DMLT','DMLT'), #Diploma in Medical Laboratory Technology
#         ('ADMLT','ADMLT'), #Associate in Medical Laboratory Technology
#         ('BMLT','BMLT'), #Bachelor of Medical Laboratory Technology
#         ('MLT','MLT'), #Medical Laboratory Technology

#     ),
#     id = models.AutoField(primary_key=True)
#     qual_name = models.CharField(max_length=100, choices=qualification_names)





class Doctor(models.Model):
    
    qualification_names = (
        ('BDS','BDS'),  #Bachelor of Dental Surgery
        ('BHMS','BHMS'), #Bachelor of Homeopathy Medicine and Surgery
        ('BPT','BPT'), #Bachelor of physiotherapy
        ('B.Pharm','B.Pharm'), #bachelor of pharma
        ('BUMS','BUMS'),  #Bachelor of Unani Medicine and Surgery
        ('MD','MD'), #doctor of medicine
        ('BYNS','BYNS'), #Bachelor of Yoga and Naturopathy Sciences
        ('DS','DS'), #doctor of surgery
        ('DCM','DCM'), #doctor of clinical medicine
        ('DPM','DPM'), #doctor of public medicine
        ('D.Pharm','D.Pharm'), #doctor of pharma
        ('MCM','MCM'), #master of clinical medicine
        ('MMSc','MMSc'), #master of medical science
        ('MPH','MPH'), #master of public health
        ('MM','MM'), #master of medicine
        ('M.Pharm','M.Pharm'), #master of pharma
        ('M.B.B.S','M.B.B.S'), #master of botany and botanical science
        ('M.Phy','M.Phy'), #master of physiotherapy
        ('M.phil','M.phil'), #master of philosophy
        ('Msc','Msc'), #master of science
        ('MS','MS'),  #master of surgery
        ('DNB','DNB'), #Diplomate of National Board
        ('M.Ch','M.Ch') #Master of Chirurgiae
    )

     # #For nurses
        # ('PN','PN'), #1. Diploma in Practical Nursing
        # ('ASN','ASN'), #2. Associate in Nursing
        # ('BSN','BSN'), #3. Bachelor of Nursing
        # ('MSN','MSN'), #4. Master of Nursing
        # ('DSN','DSN'), #5. Doctor of Nursing
        # ('B.Sc(N)','B.Sc(N)'), #8. Bachelor of Science in Nursing
        # ('M.Sc(N)','M.Sc(N)'), #9. Master of Science in Nursing
        # ('BDN','BDN'), #10. Bachelor of Dental Nursing
        # ('CNA','CNA'), #11. Certificate in Nursing Administration

        # # for laboratory
        # ('DMLT','DMLT'), #Diploma in Medical Laboratory Technology
        # ('ADMLT','ADMLT'), #Associate in Medical Laboratory Technology
        # ('BMLT','BMLT'), #Bachelor of Medical Laboratory Technology
        # ('MLT','MLT'), #Medical Laboratory Technology

    id = models.AutoField(primary_key=True)
    email = models.ForeignKey(Account, on_delete=models.CASCADE)
    year_of_service = models.IntegerField(blank=False, null=False)
    # qual_name = models.ForeignKey(Qualification, on_delete=models.CASCADE,related_name='q-realated')
    qual_name = MultiSelectField(choices=qualification_names, max_choices=5, max_length=100)
    spec_name = models.ForeignKey(Specialization, on_delete=models.CASCADE,related_name='spec_name_related')
    des_name = models.ForeignKey(Designation, on_delete=models.CASCADE,related_name='des_name_doctor')
    license_no = models.CharField(max_length=100, blank=True)
    is_doctor = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_lab = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

