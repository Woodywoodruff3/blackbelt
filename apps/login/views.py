from __future__ import unicode_literals
from .models import *
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'login/index.html')

def register(request):
    print request.POST
    errs = Users.objects.validate(request.POST)
    if errs:
        for e in errs:
            messages.error(request, e)
            
        return redirect('/main')
    else:
        #register userac
        new_user = Users.objects.create_user(request.POST)
        request.session['id'] = new_user.id
        request.session['name'] = new_user.name
        request.session['emai'] = new_user.email 
        request.session['username'] = new_user.username
    return redirect('/travels')

def login(request):
    users = results = Users.objects.check_user(request.POST)
    if results['status'] == False:
        for e in results['errors']:
            messages.error(request, e)
        return redirect("/main")
    request.session['name'] = results['user'].name
    request.session['email'] = results['user'].email
    request.session['id'] = results['user'].id
    request.session['username'] = results['user'].username
    print request.session['id']
    return redirect('/travels')

def logout(request):
    request.session.clear()
    
    return redirect('/main')