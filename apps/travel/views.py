# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.db.models import Q

# Create your views here.
def home(request):
    
    context = {
        "usertrips": Trip.objects.filter(Q(planner__id = request.session['id']) | Q(tourist__id = request.session['id'])).order_by('start_date'),
        'othertrips': Trip.objects.all().exclude(planner__id = request.session['id']).exclude(tourist__id = request.session['id']).order_by('start_date')
    }
    
    return render(request, 'travel/home.html', context)

def show(request, id):
    trip = Trip.objects.get(id=id)
    
    context = {
        'trip' : trip,
    }
    return render(request, 'travel/show.html', context)

def join(request, id):
    Trip.objects.joiner(id, request.session['id'])
    return redirect('/travels')

def add(request):
    return render(request, 'travel/add.html')

def addplan(request):
   
    errs = Trip.objects.trip_validation(request.POST)
    if errs:
        for e in errs:
            messages.error(request, e)
        return redirect('/travels/add')
    else:
        Trip.objects.addtrip(request.POST, request)
        
    return redirect('/travels')