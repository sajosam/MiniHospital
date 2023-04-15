from django.shortcuts import render

# Create your views here.



from django.shortcuts import render
from django.views.generic import View
   
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd
import calendar
import matplotlib.pyplot as plt
from doctor.models import Doctor,Specialization
   
class HomeView(View):
    def get(self, request, *args, **kwargs):
        s=Doctor.objects.get(email=request.user.id).spec_name
        context={
            'spec':s
        }
        return render(request, 'dashboard/dashhome.html',context)

class WeekdayView(View):
    def get(self, request, *args, **kwargs):
        s=Doctor.objects.get(email=request.user.id).spec_name

        context={
            'spec':s
        }
        return render(request, 'dashboard/weekday.html',context)

class GenderView(View):
    def get(self, request, *args, **kwargs):
        s=Doctor.objects.get(email=request.user.id).spec_name

        context={
            'spec':s
        }
        return render(request, 'dashboard/dashgender.html',context)
    
class AgeView(View):
    def get(self, request, *args, **kwargs):
        s=Doctor.objects.get(email=request.user.id).spec_name

        context={
            'spec':s
        }
        return render(request, 'dashboard/agedash.html',context)

class DiseaseView(View):
    def get(self, request, *args, **kwargs):
        s=Doctor.objects.get(email=request.user.id).spec_name

        context={
            'spec':s
        }
        return render(request, 'dashboard/disease.html',context)

class PredictionView(View):
    def get(self, request, *args, **kwargs):
        s=Doctor.objects.get(email=request.user.id).spec_name

        context={
            'spec':s
        }
        return render(request, 'dashboard/predict.html',context)
    
    
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

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

        count_by_month = df_2022.groupby(pd.Grouper(key='date', freq='M')).size()
        count_by_month = count_by_month.to_dict()

        print("2022",count_by_month)

        df = df[(df['year'] >= 2020) & (df['year'] <= 2022)]
        grouped = df.groupby(['year', 'month'])['id'].count().reset_index()

        # Train a machine learning model
        X_train = grouped[['year', 'month']]
        y_train = grouped['id']
        model = RandomForestRegressor(n_estimators=100)
        model.fit(X_train, y_train)

        # Make predictions
        X_test = pd.DataFrame({'year': [2023]*12 + [2024]*12, 'month': list(range(1,13))*2})
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
        s=Doctor.objects.get(email=request.user.id).spec_name
        df = pd.read_csv('dashboard/moddata.csv')
        df_spec = df[(df['specialty'] == str(s)) & (df['year'] == 2022)]

        disease_count = df_spec['disease'].unique()
        print(disease_count)

        context={
            'spec':s,
            'disease_count':disease_count

        }
        return render(request, 'dashboard/riskdash.html',context)


class ChartData(APIView):
    def get(self, request, format=None):
        df = pd.read_csv('dashboard/moddata.csv')
        s=Doctor.objects.get(email=request.user.id).spec_name
        spec=Specialization.objects.get(spec_name=s).spec_name
        # part 1
        df1 = df.loc[(df['specialty'] == spec) & (df['year']==2022)].groupby('month')['month'].count()

        # create a dictionary to map month names to month numbers
        month_dict = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
                      'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

        # sort the labels by month number
        sorted_labels = sorted(df1.index.tolist(), key=lambda x: month_dict[x])

        data={
            "labels": sorted_labels,
            "chartdata": df1.reindex(sorted_labels).values.tolist(),
        }
        print(data)
        return Response(data)



class WeekdayData(APIView):
    def get(self, request, format=None):
        df = pd.read_csv('dashboard/moddata.csv')
        s=Doctor.objects.get(email=request.user.id).spec_name
        spec=Specialization.objects.get(spec_name=s).spec_name
        df_weekday = df.loc[(df['day_type'] == 'Weekday') & (df['year']==2022)] # filter weekday data
        months = df['month'].unique()
        data = {}
        da={}
        for month in months:
            month_data = df_weekday.loc[(df_weekday['month'] == month) & (df_weekday['specialty'] == spec)]
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
            month_data = df_weekend.loc[(df_weekend['month'] == month) & (df_weekend['specialty'] == spec)]
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
        data={
            "month_key":result.keys(),
            "week":result.values(),
            "weekend":weekend.keys(),
            "week_end":weekend.values(),
        }
        return Response(data)
    

class GenderData(APIView):
    def get(self, request):
        s=Doctor.objects.get(email=request.user.id).spec_name
        spec=Specialization.objects.get(spec_name=s).spec_name
        df = pd.read_csv('dashboard/moddata.csv')
        df_gender = df.loc[(df['specialty'] == spec) & (df['year']==2022)] # filter weekday data
        months = df['month'].unique()

        data = {}
        for gender in ['Male', 'Female']:
            data[gender] = {month: df_gender.loc[(df_gender['month'] == month) & (df_gender['gender'] == gender)]['gender'].count()
                            for month in months}

        data={
            "month_key":data.keys(),
            "week":data.values(),
        }
        return Response(data)


import numpy as np
class AgeData(APIView):
    def get(self,request):
        s=Doctor.objects.get(email=request.user.id).spec_name
        spec=Specialization.objects.get(spec_name=s).spec_name
        df = pd.read_csv('dashboard/moddata.csv')
        bins = [0, 18, 25, 35, 45, 55, 65, np.inf]
        labels = ['0-18', '18-25', '25-35', '35-45', '45-55', '55-65', '65+']
        df_age_male = df.loc[(df['specialty'] == spec) & (df['gender'] == 'Male') & (df['year']==2022)]
        df_age_female = df.loc[(df['specialty']==spec) & (df['gender'] == 'Female') & (df['year']==2022)]
        male = pd.cut(df_age_male['age'], bins=bins, labels=labels).value_counts().to_dict()
        female=pd.cut(df_age_female['age'], bins=bins, labels=labels).value_counts().to_dict()

        data={
            'male':male,
            'female':female,
        }

        return Response(data)

class DiseaseData(APIView):
    def get(self, request):
        s = Doctor.objects.get(email=request.user.id).spec_name
        spec = Specialization.objects.get(spec_name=s).spec_name
        df = pd.read_csv('dashboard/moddata.csv')
        cardiology_df = df[(df['specialty'] == spec) & (df['year'] == 2022)]
        grouped = cardiology_df.groupby(['month', 'disease'])['disease'].count()
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

        diseases = cardiology_df ['disease'].unique()
        # months = cardiology_df ['month'].unique()
        risk={}
        data = {}
        for disease in diseases:
            # create a age bins
            bins = [0, 18, 25, 35, 45, 55, 65, np.inf]
            labels = ['0-18', '18-25', '25-35', '35-45', '45-55', '55-65', '65+']
            # create a new column for age group
            cardiology_df['age_group'] = pd.cut(cardiology_df['age'], bins=bins, labels=labels) 
            # risk % of ith disease based on count in each age bins
            risk = cardiology_df[cardiology_df['disease'] == disease].groupby('age_group')['age_group'].count() / cardiology_df[cardiology_df['disease'] == disease].shape[0] * 100
            # store the risk % in a dictionary
            risk = dict(zip(risk.index, risk.values))
            # store the dictionary in a list
            data[disease] = risk
        
        print(data)
        return Response(data)

  


                

