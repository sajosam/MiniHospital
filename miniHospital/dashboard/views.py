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
        # df = pd.read_csv('dashboard/moddata.csv')

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

class ChartData(APIView):
    def get(self, request, format=None):
        df = pd.read_csv('dashboard/moddata.csv')
        s=Doctor.objects.get(email=request.user.id).spec_name
        spec=Specialization.objects.get(spec_name=s).spec_name
        # part 1
        df1 = df.loc[df['specialty'] == spec].groupby('month')['month'].count()

        data={
            "labels":df1.index.tolist(),
            "chartdata":df1.values.tolist(),

        }
        return Response(data)


class WeekdayData(APIView):
    def get(self, request, format=None):
        df = pd.read_csv('dashboard/moddata.csv')
        s=Doctor.objects.get(email=request.user.id).spec_name
        spec=Specialization.objects.get(spec_name=s).spec_name
        df_weekday = df.loc[df['day_type'] == 'Weekday'] # filter weekday data
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
        df_gender = df.loc[df['specialty'] == spec] # filter weekday data
        months = df['month'].unique()
        data = {}
        da={}
        for month in months:
            month_data = df_gender.loc[df_gender['month'] == month]
            male_count = month_data[month_data['gender'] == 'Male']['gender'].count()
            female_count = month_data[month_data['gender'] == 'Female']['gender'].count()
            # data[month] = {'Male': male_count, 'Female': female_count}
        
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
        df_age_male = df.loc[(df['specialty'] == spec) & (df['gender'] == 'Male')]
        df_age_female = df.loc[(df['specialty']==spec) & (df['gender'] == 'Female')]
        male = pd.cut(df_age_male['age'], bins=bins, labels=labels).value_counts().to_dict()
        female=pd.cut(df_age_female['age'], bins=bins, labels=labels).value_counts().to_dict()
        
        data={
            'male':male,
            'female':female,
        }

        return Response(data)
