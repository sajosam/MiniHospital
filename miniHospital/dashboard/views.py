import pickle
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from django.shortcuts import render

# Create your views here.


from django.shortcuts import render
from django.views.generic import View

from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
import calendar
import matplotlib.pyplot as plt
from doctor.models import Doctor, Specialization


class HomeView(View):
    def get(self, request, *args, **kwargs):
        s = Doctor.objects.get(email=request.user.id).spec_name
        context = {
            'spec': s
        }
        return render(request, 'dashboard/dashhome.html', context)


class WeekdayView(View):
    def get(self, request, *args, **kwargs):
        s = Doctor.objects.get(email=request.user.id).spec_name

        context = {
            'spec': s
        }
        return render(request, 'dashboard/weekday.html', context)


class GenderView(View):
    def get(self, request, *args, **kwargs):
        s = Doctor.objects.get(email=request.user.id).spec_name

        context = {
            'spec': s
        }
        return render(request, 'dashboard/dashgender.html', context)


class AgeView(View):
    def get(self, request, *args, **kwargs):
        s = Doctor.objects.get(email=request.user.id).spec_name

        context = {
            'spec': s
        }
        return render(request, 'dashboard/agedash.html', context)


class DiseaseView(View):
    def get(self, request, *args, **kwargs):
        s = Doctor.objects.get(email=request.user.id).spec_name

        context = {
            'spec': s
        }
        return render(request, 'dashboard/disease.html', context)


class PredictionView(View):
    def get(self, request, *args, **kwargs):
        s = Doctor.objects.get(email=request.user.id).spec_name

        context = {
            'spec': s
        }
        return render(request, 'dashboard/predict.html', context)


class PredictionData(APIView):
    def get(self, request, format=None):
        # Load and preprocess the data
        df = pd.read_csv('dashboard/moddata.csv')
        s = Doctor.objects.get(email=request.user.id).spec_name
        spec = Specialization.objects.get(spec_name=s).spec_name
        df = df[df['specialty'] == spec]
        df['date'] = pd.to_datetime(df['date'])
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month

        df_2022 = df[df['year'] == 2022]

        count_by_month = df_2022.groupby(
            pd.Grouper(key='date', freq='M')).size()
        count_by_month = count_by_month.to_dict()

        print("2022", count_by_month)

        df = df[(df['year'] >= 2020) & (df['year'] <= 2022)]
        grouped = df.groupby(['year', 'month'])['id'].count().reset_index()

        # Train a machine learning model
        X_train = grouped[['year', 'month']]
        y_train = grouped['id']
        model = RandomForestRegressor(n_estimators=100)
        model.fit(X_train, y_train)

        # Make predictions
        X_test = pd.DataFrame(
            {'year': [2023]*12 + [2024]*12, 'month': list(range(1, 13))*2})
        y_pred = model.predict(X_test)

        # Prepare the response data
        df = grouped.groupby('month').sum().reset_index()
        df['month'] = pd.to_datetime(df['month'], format='%m').dt.month_name()
        df = df.sort_values('month')
        sorted_labels = df['month']
        data = {
            "count2023": list(y_pred[:12]),
            "count2024": list(y_pred[12:]),
            "month": sorted_labels.tolist(),
            "count2022": list(count_by_month.values())
        }

        print(data)
        return Response(data)


class RiskAnalysisView(View):
    def get(self, request, *args, **kwargs):
        s = Doctor.objects.get(email=request.user.id).spec_name
        df = pd.read_csv('dashboard/moddata.csv')
        df_spec = df[(df['specialty'] == str(s)) & (df['year'] == 2022)]

        disease_count = df_spec['disease'].unique()
        print(disease_count)

        context = {
            'spec': s,
            'disease_count': disease_count

        }
        return render(request, 'dashboard/riskdash.html', context)


class ChartData(APIView):
    def get(self, request, format=None):
        df = pd.read_csv('dashboard/moddata.csv')
        s = Doctor.objects.get(email=request.user.id).spec_name
        spec = Specialization.objects.get(spec_name=s).spec_name
        # part 1
        df1 = df.loc[(df['specialty'] == spec) & (
            df['year'] == 2022)].groupby('month')['month'].count()

        # create a dictionary to map month names to month numbers
        month_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                      'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

        # sort the labels by month number
        sorted_labels = sorted(df1.index.tolist(), key=lambda x: month_dict[x])

        data = {
            "labels": sorted_labels,
            "chartdata": df1.reindex(sorted_labels).values.tolist(),
        }
        print(data)
        return Response(data)


class WeekdayData(APIView):
    def get(self, request, format=None):
        df = pd.read_csv('dashboard/moddata.csv')
        s = Doctor.objects.get(email=request.user.id).spec_name
        spec = Specialization.objects.get(spec_name=s).spec_name
        df_weekday = df.loc[(df['day_type'] == 'Weekday') & (
            df['year'] == 2022)]  # filter weekday data
        months = df['month'].unique()
        data = {}
        da = {}
        for month in months:
            month_data = df_weekday.loc[(df_weekday['month'] == month) & (
                df_weekday['specialty'] == spec)]
            day_count = month_data.groupby('day')['day'].count()
            day_count_dict = dict(zip(day_count.index, day_count.values))
            da[month] = day_count_dict
        result = {}
        for month, data in da.items():
            for day, count in data.items():
                if day not in result:
                    result[day] = {}
                result[day][month] = count
        df_weekend = df.loc[df['day_type'] == 'Weekend']
        week = {}
        for month in months:
            month_data = df_weekend.loc[(df_weekend['month'] == month) & (
                df_weekend['specialty'] == spec)]
            print(month)
            day_count = month_data.groupby('day')['day'].count()
            day_count_dict = dict(zip(day_count.index, day_count.values))
            week[month] = day_count_dict
        weekend = {}
        for month, data in week.items():
            for day, count in data.items():
                if day not in weekend:
                    weekend[day] = {}
                weekend[day][month] = count
        data = {
            "month_key": result.keys(),
            "week": result.values(),
            "weekend": weekend.keys(),
            "week_end": weekend.values(),
        }
        return Response(data)


class GenderData(APIView):
    def get(self, request):
        s = Doctor.objects.get(email=request.user.id).spec_name
        spec = Specialization.objects.get(spec_name=s).spec_name
        df = pd.read_csv('dashboard/moddata.csv')
        df_gender = df.loc[(df['specialty'] == spec) & (
            df['year'] == 2022)]  # filter weekday data
        months = df['month'].unique()

        data = {}
        for gender in ['Male', 'Female']:
            data[gender] = {month: df_gender.loc[(df_gender['month'] == month) & (df_gender['gender'] == gender)]['gender'].count()
                            for month in months}

        data = {
            "month_key": data.keys(),
            "week": data.values(),
        }
        return Response(data)


class AgeData(APIView):
    def get(self, request):
        s = Doctor.objects.get(email=request.user.id).spec_name
        spec = Specialization.objects.get(spec_name=s).spec_name
        df = pd.read_csv('dashboard/moddata.csv')
        bins = [0, 18, 25, 35, 45, 55, 65, np.inf]
        labels = ['0-18', '18-25', '25-35', '35-45', '45-55', '55-65', '65+']
        df_age_male = df.loc[(df['specialty'] == spec) & (
            df['gender'] == 'Male') & (df['year'] == 2022)]
        df_age_female = df.loc[(df['specialty'] == spec) & (
            df['gender'] == 'Female') & (df['year'] == 2022)]
        male = pd.cut(df_age_male['age'], bins=bins,
                      labels=labels).value_counts().to_dict()
        female = pd.cut(df_age_female['age'], bins=bins,
                        labels=labels).value_counts().to_dict()

        data = {
            'male': male,
            'female': female,
        }

        return Response(data)


class DiseaseData(APIView):
    def get(self, request):
        s = Doctor.objects.get(email=request.user.id).spec_name
        spec = Specialization.objects.get(spec_name=s).spec_name
        df = pd.read_csv('dashboard/moddata.csv')
        cardiology_df = df[(df['specialty'] == spec) & (df['year'] == 2022)]
        grouped = cardiology_df.groupby(['month', 'disease'])[
            'disease'].count()
        print("groped", grouped)

        # Initialize result dictionary with all diseases
        diseases = cardiology_df['disease'].unique()
        months = cardiology_df['month'].unique()
        result = {}
        for month in months:
            result[month] = {}
            for disease in diseases:
                result[month][disease] = 0

        # Update result dictionary with counts for each disease and month
        for month, disease in grouped.index:
            count = grouped.loc[(month, disease)]
            result[month][disease] = count

        # Initialize new_result dictionary with all diseases
        new_result = {}
        for disease in diseases:
            new_result[disease] = {}
            for month in months:
                new_result[disease][month] = result[month][disease]

        print(new_result)

        data = {
            'disease': list(diseases),
            'month': list(months),
            'result': list(new_result.values()),
        }

        return Response(data)


class RiskAnalysisData(APIView):
    def get(self, request):

        s = Doctor.objects.get(email=request.user.id).spec_name
        spec = Specialization.objects.get(spec_name=s).spec_name
        df = pd.read_csv('dashboard/moddata.csv')
        cardiology_df = df[(df['specialty'] == spec) & (df['year'] == 2022)]

        diseases = cardiology_df['disease'].unique()
        # months = cardiology_df ['month'].unique()
        risk = {}
        data = {}
        for disease in diseases:
            # create a age bins
            bins = [0, 18, 25, 35, 45, 55, 65, np.inf]
            labels = ['0-18', '18-25', '25-35',
                      '35-45', '45-55', '55-65', '65+']
            # create a new column for age group
            cardiology_df['age_group'] = pd.cut(
                cardiology_df['age'], bins=bins, labels=labels)
            # risk % of ith disease based on count in each age bins
            risk = cardiology_df[cardiology_df['disease'] == disease].groupby('age_group')[
                'age_group'].count() / cardiology_df[cardiology_df['disease'] == disease].shape[0] * 100
            # store the risk % in a dictionary
            risk = dict(zip(risk.index, risk.values))
            # store the dictionary in a list
            data[disease] = risk

        print(data)
        return Response(data)


def effectiveness(request):
    if request.method == 'POST':
        condition = request.POST.get('condition')
        type = request.POST.get('type')
        form = request.POST.get('form')
        indication = request.POST.get('indication')
        drug = request.POST.get('drug')
        price = int(request.POST.get('price'))
        easeofuse = int(request.POST.get('easeofuse'))
        reviews = int(request.POST.get('reviews'))
        satisfaction = int(request.POST.get('satisfaction'))
        print(condition, type, form, indication, drug)

        type_mapping = {0: 'OTC', 1: 'RX', 2: 'RX/OTC'}
        type_mapping = {v: k for k, v in type_mapping.items()}
        form_mapping = {0: 'Capsule', 1: 'Cream',
                        2: 'Liquid (Drink)', 3: 'Liquid (Inject)', 4: 'Other', 5: 'Tablet'}
        form_mapping = {v: k for k, v in form_mapping.items()}
        indication_mapping = {0: 'Off Label', 1: 'On Label'}
        indication_mapping = {v: k for k, v in indication_mapping.items()}
        condition_mapping = {0: 'Acute Bacterial Sinusitis', 1: 'Atopic Dermatitis', 2: 'Bacterial Conjunctivitis', 3: 'Bacterial Urinary Tract Infection', 4: 'Infantile Autism', 5: 'Influenza', 6: 'Pharyngitis due to Streptococcus Pyogenes', 7: 'Sleepiness Due To Obstructive Sleep Apnea', 8: 'adenocarcinoma of pancreas', 9: 'back pain', 10: 'biliary calculus', 11: 'chickenpox', 12: 'colorectal cancer', 13: 'depression', 14: 'diverticulitis of gastrointestinal tract', 15: 'edema',
                             16: 'endometriosis', 17: 'fever', 18: 'fibromyalgia', 19: 'flatulence', 20: 'furunculosis', 21: 'gastroesophageal reflux disease', 22: 'genital herpes simplex', 23: 'gout', 24: 'hemorrhoids', 25: 'herpes zoster', 26: 'hypercholesterolemia', 27: 'hypertension', 28: 'impetigo', 29: "meniere's disease", 30: 'oral candidiasis', 31: 'prevention of cerebrovascular accident', 32: 'pyelonephritis', 33: 'scabies', 34: 'sore throat', 35: 'vertigo', 36: 'vulvovaginal candidiasis'}
        condition_mapping = {v: k for k, v in condition_mapping.items()}
        drug_mapping = {0: 'ASA-Acetaminophen-Salicyl-Caff', 1: 'ASA-Acetaminophen-Salicyl-Caff, Mg Salicylat-Acetaminophen-Caf', 2: 'Acebutolol', 3: 'Acetaminophen', 4: 'Acetaminophen-Caffeine', 5: 'Acetaminophen-DM', 6: 'Acetaminophen-Pamabrom, Ibuprofen', 7: 'Acetazolamide', 8: 'Acetohydroxamic Acid', 9: 'Activated Charcoal-Simethicone, Simethicone', 10: 'Acyclovir', 11: 'Acyclovir Sodium', 12: 'Acyclovir-Hydrocortisone', 13: 'Al Hyd-Mg Tr-Alg Ac-Sod Bicarb', 14: 'Al Hyd-Mg Tr-Alg Ac-Sod Bicarb, Aluminum Hydrox-Magnesium Carb, Aluminum-Magnesium-Alginate', 15: 'Al Hyd-Mg Tr-Alg Ac-Sod Bicarb, Aluminum Hydrox-Magnesium Carb, Aluminum-Magnesium-Alginate, Calcium Carbonate', 16: 'Al Hyd-Mg Tr-Alg Ac-Sod Bicarb, Magaldrate, Aluminum-Magnesium Hydroxide, Calcium Carbonate-Mag Hydroxid, Aluminum Hydrox-Magnesium Carb, Calcium And Magnesium Carbonat, Aluminum-Magnesium-Alginate, Calcium Carbonate, Dihydroxyaluminum Sod Carb, Alum-Mag Hydroxide-Simeth', 17: 'Alclometasone', 18: 'Alirocumab', 19: 'Aliskiren', 20: 'Alum-Mag Hydroxide-Simeth', 21: 'Alum-Mag Hydroxide-Simeth, Calcium Carbonate-Simethicone', 22: 'Aluminum Hydrox-Magnesium Carb', 23: 'Aluminum Hydroxide Gel', 24: 'Aluminum-Magnesium Hydroxide', 25: 'Aluminum-Magnesium Hydroxide, Alum-Mag Hydroxide-Simeth', 26: 'Aluminum-Magnesium Hydroxide, Aluminum Hydrox-Magnesium Carb, Dihydroxyaluminum Sod Carb, Alum-Mag Hydroxide-Simeth', 27: 'Aluminum-Magnesium Hydroxide, Calcium Carbonate, Alum-Mag Hydroxide-Simeth', 28: 'Aluminum-Magnesium Hydroxide, Calcium Carbonate-Mag Hydroxid, Calcium And Magnesium Carbonat, Calcium Carbonate, Alum-Mag Hydroxide-Simeth', 29: 'Aluminum-Magnesium-Alginate, Alum-Mag Hydroxide-Simeth', 30: 'Amcinonide', 31: 'Amikacin', 32: 'Amiloride-Hydrochlorothiazide', 33: 'Amitriptyline', 34: 'Amlodipine', 35: 'Amlodipine-Atorvastatin', 36: 'Amlodipine-Benazepril', 37: 'Amlodipine-Olmesartan', 38: 'Amlodipine-Valsartan', 39: 'Amlodipine-Valsartan-Hcthiazid', 40: 'Amoxapine', 41: 'Amoxicillin', 42: 'Amoxicillin-Pot Clavulanate', 43: 'Ampicillin', 44: 'Ampicillin Sodium', 45: 'Ampicillin-Sulbactam', 46: 'Aripiprazole', 47: 'Armodafinil', 48: 'Aspirin', 49: 'Aspirin, Buffered', 50: 'Aspirin-Acetaminophen-Caffeine', 51: 'Aspirin-Acetaminophen-Caffeine, Aspirin, Phenyltoloxamine-Acetaminophen', 52: 'Aspirin-Calcium Carbonate', 53: 'Atenolol', 54: 'Atenolol-Chlorthalidone', 55: 'Atorvastatin', 56: 'Azilsartan Med-Chlorthalidone', 57: 'Azilsartan Medoxomil', 58: 'Azithromycin', 59: 'Aztreonam', 60: 'Bacitracin', 61: 'Bacitracin-Polymyxin B', 62: 'Benazepril', 63: 'Benazepril-Hydrochlorothiazide', 64: 'Benzocaine', 65: 'Besifloxacin', 66: 'Betamethasone Acet,Sod Phos', 67: 'Betamethasone Dipropionate', 68: 'Betamethasone Valerate', 69: 'Betamethasone, Augmented', 70: 'Betamethasone, Augmented, Betamethasone Dipropionate', 71: 'Betaxolol', 72: 'Bismuth Subg-Balsam-Znox-Resor, Starch, Pramoxine-Mineral Oil-Zinc', 73: 'Bisoprolol Fumarate', 74: 'Bisoprolol-Hydrochlorothiazide', 75: 'Bumetanide', 76: 'Butoconazole Nitrate', 77: 'Calcium Carb-Mag Hydrox-Simeth, Alum-Mag Hydroxide-Simeth', 78: 'Calcium Carbonate-Mag Hydroxid', 79: 'Calcium Carbonate-Mag Hydroxid, Alum-Mag Hydroxide-Simeth', 80: 'Calcium Carbonate-Mag Hydroxid, Calcium Carbonate, Dihydroxyaluminum Sod Carb', 81: 'Calcium Carbonate-Mag Hydroxid, Dihydroxyaluminum Sod Carb', 82: 'Calcium Carbonate-Simethicone', 83: 'Candesartan', 84: 'Candesartan-Hydrochlorothiazid', 85: 'Capecitabine', 86: 'Capsaicin', 87: 'Capsaicin In Castor Oil', 88: 'Capsaicin-Camphor-Menthol', 89: 'Capsaicin-Menthol, Capsaicin', 90: 'Capsaicin-Methyl Sal-Menthol', 91: 'Captopril', 92: 'Captopril-Hydrochlorothiazide', 93: 'Carvedilol', 94: 'Carvedilol Phosphate', 95: 'Cefaclor', 96: 'Cefadroxil', 97: 'Cefazolin', 98: 'Cefazolin In Dextrose (Iso-Os)', 99: 'Cefdinir', 100: 'Cefditoren Pivoxil', 101: 'Cefepime', 102: 'Cefepime In Dextrose,Iso-Osm', 103: 'Cefixime', 104: 'Cefpodoxime', 105: 'Cefprozil', 106: 'Ceftazidime', 107: 'Ceftriaxone', 108: 'Ceftriaxone In Dextrose,Iso-Os', 109: 'Cefuroxime Axetil', 110: 'Cefuroxime Sodium', 111: 'Celecoxib', 112: 'Cephalexin', 113: 'Cetirizine', 114: 'Chlorothiazide', 115: 'Chlorphen-PE-DM-Acetaminophen, Cpm-Pseudoeph-DM-Acetaminophen', 116: 'Chlorphenir-Phenylephrn-Aspirn, Diphenhydramine-Acetaminophen, Cpm-Phenyleph-Acetaminophen, Cpm-Pseudoeph-DM-Acetaminophen', 117: 'Chlorpheniram-DM-Acetaminophen', 118: 'Chlorpheniramine-Acetaminophen', 119: 'Chlorpheniramine-Acetaminophen, Chlorphen-PPA-Acetaminophen', 120: 'Chlorthalidone', 121: 'Cholestyramine (With Sugar)', 122: 'Cholestyramine-Aspartame', 123: 'Choline,Magnesium Salicylate', 124: 'Cimetidine', 125: 'Cimetidine Hcl', 126: 'Ciprofloxacin', 127: 'Ciprofloxacin Hcl', 128: 'Ciprofloxacin Hcl, Ciprofloxacin', 129: 'Ciprofloxacin In 5 % Dextrose', 130: 'Cisplatin', 131: 'Clarithromycin', 132: 'Clindamycin In 5 % Dextrose', 133: 'Clindamycin Phosphate', 134: 'Clobetasol', 135: 'Clobetasol-Emollient', 136: 'Clomipramine', 137: 'Clonidine', 138: 'Clonidine Hcl', 139: 'Clotrimazole', 140: 'Cocoa Butter-Zinc Oxide, Zinc Oxide', 141: 'Colestipol', 142: 'Cortisone', 143: 'Cpm-PPA-DM-Acetaminophen', 144: 'Cpm-PPA-DM-Acetaminophen, Acetaminophen', 145: 'Cpm-Pseudoeph-DM-Acetaminophen', 146: 'Crotamiton', 147: 'Cyclobenzaprine', 148: 'DM-Benzocaine-Menthol', 149: 'DM-PE-Acetam/DM-Acetam-Doxylam', 150: 'Danazol', 151: 'Demeclocycline', 152: 'Desipramine', 153: 'Desonide', 154: 'Desonide-Emollient Combo No 28', 155: 'Desonide-Emollient Combo No 28, Desonide', 156: 'Desoximetasone', 157: 'Dexamethasone', 158: 'Dexamethasone Sodium Phos (PF)', 159: 'Dexamethasone Sodium Phosphate', 160: 'Dexlansoprazole', 161: 'Dextromethorphan-Benzocaine', 162: 'Dextromethorphan-Guaifenesin, Guaifenesin, Cpm-Pseudoeph-DM-Acetaminophen', 163: 'Diclofenac Potassium', 164: 'Diclofenac Sodium', 165: 'Diclofenac-Misoprostol', 166: 'Diflorasone', 167: 'Diflorasone-Emollient', 168: 'Diflunisal', 169: 'Diltiazem Hcl', 170: 'Dimenhydrinate', 171: 'Diphenhydramine Citrate', 172: 'Diphenhydramine Hcl', 173: 'Diphenhydramine Hcl, Clemastine-Phenylprop, Triprolidine-Pseudoephedrine', 174: 'Diphenhydramine Hcl, Dextromethorphan-Guaifenesin, Dextromethorphan Hbr', 175: 'Diphenhydramine Hcl, Diphenhydramine Citrate', 176: 'Diphenhydramine-Calamine, Pramoxine-Calamine', 177: 'Doxazosin', 178: 'Doxepin', 179: 'Doxorubicin', 180: 'Doxycycline Calcium', 181: 'Doxycycline Calcium, Doxycycline Hyclate, Doxycycline Monohydrate', 182: 'Doxycycline Hyclate', 183: 'Doxycycline Monohydrate', 184: 'Doxylam-PE-DM-Acetaminophen-GG', 185: 'Doxylamin-PSE-DM-Acetaminophen', 186: 'Doxylamin-PSE-DM-Acetaminophen, Chlorphen-PE-DM-Acetaminophen', 187: 'Doxylamine-DM-Acetaminophen', 188: 'Doxylamine-PE-DM-Acetaminophen', 189: 'Doxylamine-PE-DM-Acetaminophen, Diphenhydramine-PPA-ASA', 190: 'Duloxetine', 191: 'Enalapril Maleate', 192: 'Enalapril-Hydrochlorothiazide', 193: 'Eplerenone', 194: 'Eprosartan', 195: 'Erythromycin', 196: 'Erythromycin Ethylsuccinate', 197: 'Erythromycin Stearate', 198: 'Esomeprazole Magnesium', 199: 'Esomeprazole Strontium', 200: 'Ethacrynic Acid', 201: 'Etodolac', 202: 'Evolocumab', 203: 'Ezetimibe', 204: 'Ezetimibe-Simvastatin', 205: 'Famciclovir', 206: 'Famotidine', 207: 'Famotidine-Ca Carb-Mag Hydrox', 208: 'Felodipine', 209: 'Fenofibrate', 210: 'Fenofibrate Micronized', 211: 'Fenofibrate Micronized, Fenofibrate', 212: 'Fenofibrate Micronized, Fenofibrate Nanocrystallized', 213: 'Fenofibrate Nanocrystallized', 214: 'Fenofibric Acid', 215: 'Fenofibric Acid (Choline)', 216: 'Fenoprofen', 217: 'Fluconazole', 218: 'Fluocinolone', 219: 'Fluocinolone And Shower Cap',
                        220: 'Fluocinolone-Emol Cmb#65', 221: 'Fluocinolone-Skin Clnsr28', 222: 'Fluocinonide', 223: 'Fluocinonide-Emollient', 224: 'Fluorouracil', 225: 'Flurandrenolide', 226: 'Flurbiprofen', 227: 'Fluticasone Propionate', 228: 'Fluvastatin', 229: 'Fluvoxamine', 230: 'Fosfomycin Tromethamine', 231: 'Fosinopril', 232: 'Fosinopril-Hydrochlorothiazide', 233: 'Furosemide', 234: 'Gatifloxacin', 235: 'Gemcitabine', 236: 'Gentamicin', 237: 'Gentamicin-Prednisolone', 238: 'Goserelin', 239: 'Guanfacine', 240: 'Halobetasol Propionate', 241: 'Hydralazine', 242: 'Hydrochlorothiazide', 243: 'Hydrocortisone', 244: 'Hydrocortisone Acetate', 245: 'Hydrocortisone Acetate, Bismuth Subg-Balsam-Znox-Resor', 246: 'Hydrocortisone Acetate, Hydrocortison-Resor-Bismth-Zno, Hydrocortisone', 247: 'Hydrocortisone Butyr-Emollient', 248: 'Hydrocortisone Butyrate', 249: 'Hydrocortisone Probutate', 250: 'Hydrocortisone Sod Succ (PF)', 251: 'Hydrocortisone Sod Succinate', 252: 'Hydrocortisone Valerate', 253: 'Hydrocortisone, Pramoxine-Benzyl Alcohol', 254: 'Hydrocortisone-Iodoquinl-Aloe2', 255: 'Hydrocortisone-Iodoquinol', 256: 'Hydrocortisone-Oatmeal-Aloe-E', 257: 'Hydrocortisone-Pramoxine, Hydrocortisone', 258: 'Ibuprofen', 259: 'Ibuprofen-Famotidine', 260: 'Imipenem-Cilastatin', 261: 'Imipramine Hcl', 262: 'Imipramine Pamoate', 263: 'Indapamide', 264: 'Indomethacin', 265: 'Irbesartan-Hydrochlorothiazide', 266: 'Isradipine', 267: 'Ketoprofen', 268: 'L Norgest/E.Estradiol-E.Estrad', 269: 'Labetalol', 270: 'Lansoprazole', 271: 'Levofloxacin', 272: 'Levofloxacin In D5W', 273: 'Levonorg-Eth Estrad Triphasic', 274: 'Levonorgestrel-Ethinyl Estrad', 275: 'Lidocaine', 276: 'Lidocaine-Hydrocortisone-Aloe', 277: 'Lindane', 278: 'Lisinopril', 279: 'Lisinopril-Hydrochlorothiazide', 280: 'Losartan', 281: 'Losartan-Hydrochlorothiazide', 282: 'Lovastatin', 283: 'Magaldrate', 284: 'Magnesium Hydroxide', 285: 'Magnesium Oxide', 286: 'Maprotiline', 287: 'Meclizine', 288: 'Meclofenamate', 289: 'Medroxyprogesterone', 290: 'Mefenamic Acid', 291: 'Meloxicam', 292: 'Menthol', 293: 'Menthol, Camphor-Methyl Salicyl-Menthol', 294: 'Menthol, Capsaicin', 295: 'Menthol-Camphor-Antarth Cb#1, Methyl Salicylate-Menthol, Camphor-Menthol, Camphor-Methyl Salicyl-Menthol', 296: 'Meropenem', 297: 'Methyldopa', 298: 'Methyldopa-Hydrochlorothiazide', 299: 'Methylprednisolone', 300: 'Methylprednisolone Acetate', 301: 'Metoclopramide Hcl', 302: 'Metolazone', 303: 'Metoprolol Su-Hydrochlorothiaz', 304: 'Metoprolol Succinate', 305: 'Metoprolol Ta-Hydrochlorothiaz', 306: 'Metoprolol Tartrate', 307: 'Metronidazole', 308: 'Metronidazole In Nacl (Iso-Os)', 309: 'Miconazole Nitrate', 310: 'Miconazole-Skin Clnsr17', 311: 'Milnacipran', 312: 'Minocycline', 313: 'Minoxidil', 314: 'Mirtazapine', 315: 'Mitomycin', 316: 'Modafinil', 317: 'Moexipril', 318: 'Mometasone', 319: 'Moxifloxacin', 320: 'Moxifloxacin-Sod.Chloride(Iso)', 321: 'Mupirocin', 322: 'Mupirocin Calcium, Mupirocin', 323: 'Nadolol', 324: 'Nafarelin', 325: 'Naproxen', 326: 'Naproxen Sodium', 327: 'Naproxen-Pseudoephedrine', 328: 'Nebivolol', 329: 'Neomycin-Bacitracin-Polymyxin', 330: 'Neomycin-Polymyxin-Gramicidin', 331: 'Niacin', 332: 'Nicardipine', 333: 'Nifedipine', 334: 'Nisoldipine', 335: 'Nitrofurantoin', 336: 'Nitrofurantoin Macrocrystal', 337: 'Nitrofurantoin Monohyd/M-Cryst', 338: 'Nizatidine', 339: 'Noreth-Ethinyl Estradiol-Iron', 340: 'Norethin-E.Estradiol Triphasic', 341: 'Norethin-E.Estradiol Triphasic, Norethindrone-Ethin Estradiol', 342: 'Norethin-Eth Estrad Biphasic', 343: 'Norethindrone Ac-Eth Estradiol', 344: 'Norethindrone Acetate', 345: 'Norethindrone-E.Estradiol-Iron', 346: 'Norethindrone-Ethin Estradiol', 347: 'Norgestimate-Ethinyl Estradiol', 348: 'Norgestrel-Ethinyl Estradiol', 349: 'Nortriptyline', 350: 'Nystatin', 351: 'Ofloxacin', 352: 'Olmesartan', 353: 'Olmesartan-Amlodipin-Hcthiazid', 354: 'Omeprazole', 355: 'Omeprazole Magnesium', 356: 'Omeprazole, Omeprazole Magnesium', 357: 'Omeprazole-Sodium Bicarbonate', 358: 'Oseltamivir', 359: 'Oxaliplatin', 360: 'Oxaprozin', 361: 'Paclitaxel-Protein Bound', 362: 'Paliperidone', 363: 'Pantoprazole', 364: 'Paroxetine Hcl', 365: 'Penicillin G Benzathin,Procain', 366: 'Penicillin G Benzathine', 367: 'Penicillin V Potassium', 368: 'Perindopril Erbumine', 369: 'Perindopril-Amlodipine', 370: 'Permethrin', 371: 'Phenelzine', 372: 'Phenyleph-DM-Acetamin-Guaifen', 373: 'Phenyleph-Min Oil-Petrolatum', 374: 'Phenyleph-Pramoxin-Glycr-W.Pet', 375: 'Phenyleph-Shark Oil-Cocoa Butr, Skin Rsp Ftr-Srk Liv-Phenylmer, Phenyleph-Shark Liv Oil-Mo-Pet', 376: 'Phenyleph-Shark Oil-Glyc-Pet, Phenyleph-Min Oil-Petrolatum, Cocoa Butter-Shark Liver Oil', 377: 'Phenylephrine Hcl', 378: 'Phenylephrine Hcl, Bismuth Subg-Balsam-Znox-Resor', 379: 'Phenylephrine-Cocoa Butter', 380: 'Phenylephrine-DM-Acetaminophen', 381: 'Phenylephrine-Witch Hazel', 382: 'Phenylephrine-Zinc Oxide, Phenylephrn-Pramoxine-Mo-W.Pet', 383: 'Phenyltoloxamine-Acetaminophen', 384: 'Pimecrolimus', 385: 'Pindolol', 386: 'Piperacillin-Tazobactam', 387: 'Piroxicam', 388: 'Pitavastatin Calcium', 389: 'Pramipexole', 390: 'Pramoxine', 391: 'Pramoxine-Calamine', 392: 'Pramoxine-Calamine-Camphor, Pramoxine-Calamine', 393: 'Pramoxine-Zinc Acetate', 394: 'Pramoxine-Zinc Oxide', 395: 'Pravastatin', 396: 'Prazosin', 397: 'Prednicarbate', 398: 'Prednisolone', 399: 'Prednisolone Sodium Phosphate', 400: 'Prednisolone, Prednisolone Sodium Phosphate', 401: 'Prednisone', 402: 'Pregabalin', 403: 'Propranolol', 404: 'Propranolol-Hydrochlorothiazid', 405: 'Protriptyline', 406: 'Pseudoeph-DM-GG-Acetaminophen', 407: 'Pseudoeph-DM-GG-Acetaminophen, Chlorphen-PE-DM-Acetaminophen', 408: 'Pseudoeph-DM-GG-Acetaminophen, Cpm-Pseudoeph-DM-Acetaminophen', 409: 'Pseudoephed-DM-Acetaminophen', 410: 'Pseudoephed-DM-Acetaminophen, Cpm-Pseudoeph-DM-Acetaminophen', 411: 'Pseudoephed-DM-Acetaminophen, Phenylpropanolamine-GG, Chlorpheniramine-Pseudoephed', 412: 'Pseudoephedrine-Ibuprofen', 413: 'Pseudoephedrine-Ibuprofen, Brompheniram-PSE-Acetaminophen', 414: 'Pseudoephedrine-Ibuprofen, Ibuprofen', 415: 'Quinapril', 416: 'Quinapril-Hydrochlorothiazide', 417: 'Rabeprazole', 418: 'Ramipril', 419: 'Ranitidine Hcl', 420: 'Retapamulin', 421: 'Risperidone', 422: 'Rosuvastatin', 423: 'Salicylic Acid, Hydrocortisone', 424: 'Simethicone', 425: 'Simethicone, Alpha-D-Galactosidase', 426: 'Simvastatin', 427: 'Spironolacton-Hydrochlorothiaz', 428: 'Spironolactone', 429: 'Starch, Pramoxine-Mineral Oil-Zinc', 430: 'Streptomycin', 431: 'Sucralfate', 432: 'Sulfacetamide Sodium', 433: 'Sulfacetamide-Prednisolone', 434: 'Sulfadiazine', 435: 'Sulfamethoxazole-Trimethoprim', 436: 'Tacrolimus', 437: 'Telmisartan', 438: 'Telmisartan-Amlodipine', 439: 'Telmisartan-Hydrochlorothiazid', 440: 'Terazosin', 441: 'Terconazole', 442: 'Tigecycline', 443: 'Timolol Maleate', 444: 'Tioconazole', 445: 'Tolmetin', 446: 'Torsemide', 447: 'Tramadol-Acetaminophen', 448: 'Trandolapril', 449: 'Trandolapril-Verapamil', 450: 'Triamcinolone Acetonide', 451: 'Triamcinolone-Emollient Comb86', 452: 'Triamterene', 453: 'Triamterene-Hydrochlorothiazid', 454: 'Triamterene-Hydrochlorothiazid, Trichlormethiazide', 455: 'Trimethoprim', 456: 'Triptorelin Pamoate', 457: 'Trolamine Salicylate', 458: 'Trolamine Salicylate, Ala-Bos-Gin-Bas-Rose-Tur-Wil', 459: 'Trolamine Salicylate-Aloe Vera', 460: 'Ursodiol', 461: 'Valacyclovir', 462: 'Valsartan', 463: 'Valsartan-Hydrochlorothiazide', 464: 'Verapamil', 465: 'Vit E-Glycerin-Dimethicone', 466: 'Vit E-Glycerin-Dimethicone, Glycerin-Dimethicone-Petro, Wh', 467: 'Vit E-Grape-Hyaluronate Sodium', 468: 'Zanamivir', 469: 'Zinc Oxide'}
        drug_mapping = {v: k for k, v in drug_mapping.items()}

        type_encoded = type_mapping[type]
        indication_encoded = indication_mapping[indication]
        form_encoded = form_mapping[form]
        drug_encoded = drug_mapping[drug]
        condition_encoded = condition_mapping[condition]

        lr = pickle.load(open('dashboard/lr.pkl', 'rb'))
        dtree = pickle.load(open('dashboard/dtree.pkl', 'rb'))
        rf = pickle.load(open('dashboard/rf.pkl', 'rb'))
        xgb = pickle.load(open('dashboard/xgb.pkl', 'rb'))

        datas = np.array([[condition_encoded, drug_encoded, easeofuse, form_encoded,
                         indication_encoded, price, reviews, satisfaction, type_encoded]])
        ensemble_pred = (lr.predict(datas) + dtree.predict(datas) +
                         rf.predict(datas) + xgb.predict(datas)) / 4

        context = {
            'condition': condition,
            'drug': drug,
            'easeofuse': easeofuse,
            'form': form,
            'indication': indication,
            'price': price,
            'reviews': reviews,
            'satisfaction': satisfaction,
            'type': type,
            'ensemble_pred': (ensemble_pred/5)*100,
        }
        return render(request, 'dashboard/efficency.html', context=context)

    else:
        data = pd.read_csv('dashboard/dataset.csv')
        for column in data.columns:
            data[column].replace(
                '\r\r\n', data[column].mode()[0], inplace=True)
        Condition = data['Condition'].unique()
        Type = data['Type'].unique()
        Form = data['Form'].unique()
        Indication = data['Indication'].unique()
        Drug = data['Drug'].unique()

        context = {
            'condition': Condition,
            'type': Type,
            'form': Form,
            'indication': Indication,
            'drug': Drug,
        }

    return render(request, 'dashboard/efficency.html', context=context)
