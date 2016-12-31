from rest_framework import viewsets
from rest_framework.decorators import detail_route,permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import render, redirect
from assignment.models import *
api_key='58f99ad3273a0d42ef51f75d64ac8e32'
from geopy.geocoders import Nominatim
import json,requests
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,timedelta
class weather(viewsets.ViewSet):
    @detail_route(methods=['GET','POST'])
    def index(self,request,pk=None):
            stationobj=station.objects.all()
            if request.method=="POST":
                wchart=display(request.data)

                return render(request,'abc.html',{"station":stationobj,"chart":wchart['data'],"title":wchart['title']})
            d={"wtype":"Temperature","station":"28.6138967,77.2159562","dfrom":datetime.now().strftime("%m/%d/%Y %H:%M %p"),"dto":(datetime.now()+ timedelta(days=2)).strftime("%m/%d/%Y %H:%M %p")}
            wchart=display(d)
            return render(request,'abc.html',{"station":stationobj,"chart":wchart['data'],"title":wchart['title']})
    @permission_classes(AllowAny)
    @detail_route(methods=['POST'])
    def addstation(self,request,pk=None):
        try:
            d=request.data
            a=d['city']+' '+d['statecode']+' '+d['country']
            geolocator = Nominatim()
            location = geolocator.geocode(a)
            stationobj=station.objects.create(city=d['city'],country=d['country'],statecode=d['statecode'],lat=location.latitude,long=location.longitude)
            stationobj.save()
            return redirect("/web/aa/1/index/")
        except Exception as e:
            print(e)
            return redirect("/web/aa/1/index/")


@csrf_exempt
def display(d):
        try:
            print(d['station'])
            a=requests.get('https://api.darksky.net/forecast/58f99ad3273a0d42ef51f75d64ac8e32/'+d['station'])
            chart=[]

            ab=json.loads(a.content.decode('utf-8'))
            for i in ab['hourly']['data']:
                temp_time = datetime.fromtimestamp(float(i['time'])).strftime('%Y-%m-%d %H:%M')
                t2= datetime.strptime(temp_time, "%Y-%m-%d %H:%M")
                if datetime.strptime(d['dfrom'], "%m/%d/%Y %H:%M %p") <= t2 and datetime.strptime(d['dto'],"%m/%d/%Y %H:%M %p" ) >= t2:
                    d1={}
                    print(temp_time)
                    if d['wtype']=="Temperature":
                        Celsius = (i['temperature'] - 32) * 5.0/9.0
                        d1.update({'y':float(format(Celsius, '.2f')),'x':temp_time})
                        chart.append(d1)
                    elif d['wtype']=="Humidity":
                        d1.update({'y':float(i['humidity']),'x':temp_time})
                        chart.append(d1)
            return {"data":chart,"title":d['wtype']}
        except Exception as e:
            return {"status":"false"}


