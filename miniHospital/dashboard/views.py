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


class ChartData(APIView):
    def get(self, request, format=None):
        df = pd.read_csv('dashboard/moddata.csv')
        s=Doctor.objects.get(email=request.user.id).spec_name
        spec=Specialization.objects.get(spec_name=s).spec_name
        df1 = df.loc[df['specialty'] == spec].groupby('month')['month'].count()

        df_weekday = df.loc[df['day_type'] == 'Weekday'] # filter weekday data
        months = df['month'].unique() # get unique months in the dataset
        data = {}
        da={}
        for month in months:
            month_data = df_weekday.loc[(df_weekday['month'] == month) & (df_weekday['specialty'] == spec)]
            day_count = month_data.groupby('day')['day'].count()
            day_count_dict = dict(zip(day_count.index, day_count.values))
            da[month] = day_count_dict
        
        # convert da to the desired format
        result = {}
        for month, data in da.items():
            for day, count in data.items():
                if day not in result:
                    result[day] = {}
                result[day][month] = count
        
        print(result)
        
        
        data={
            "labels":df1.index.tolist(),
            "chartdata":df1.values.tolist(),
            "month_key":result.keys(),
            "week":result.values()
        }
        return Response(data)
