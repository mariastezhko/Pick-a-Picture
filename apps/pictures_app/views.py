from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import random


import bcrypt
from models import *


def index(request):
    if request=='POST':
        return redirect('/')
    else:
        data = Image.objects.image_processor()
        return render(request, 'pictures_app/index.html', data)

def renderForm(request):
    try:
        request.session['user_id']
        return render(request, 'pictures_app/upload.html')
    except:
        return redirect('/login')


def submitCriteria(request):
    Criteria.objects.create(name=request.POST['name'])
    return redirect('/upload')


def submitSubcategory(request):
    subcategory = Subcategory.objects.create(name=request.POST['name'])
    criteria = Criteria.objects.get(name=request.POST['criteria'])
    criteria.subcategories.add(subcategory)
    return redirect('/upload')


def submitImage(request):
    subcategory = Subcategory.objects.get(name=request.POST['subcategory'])
    image = Image.objects.create(image=request.FILES['image'], name=request.POST['name'])
    subcategory.images.add(image)
    return redirect('/upload')


def processRegistration(request):
    if request.method == 'POST':
        print "goto validation"
        new_user = User.objects.user_validator(request.POST)
        print new_user
        if new_user[0] == True:
            messages.success(request, 'Welcome, ' + new_user[1].name)
            request.session['user_id'] = new_user[1].id
            return redirect('/upload')
        else:
            for error in new_user[1]:
                messages.error(request, error)
            return redirect('/login')
    else:
        return render(request, 'pictures_app/register.html')


def processLogin(request):
    if request.method == 'POST':
        this_user = User.objects.login_validator(request.POST)
        if this_user[0] == True:
            messages.success(request, 'Welcome, ' + this_user[1].name)
            request.session['user_id'] = this_user[1].id
            return redirect('/upload')
        else:
            for error in this_user[1]:
                messages.error(request, error)
            return redirect('/login')
    else:
        return render(request, 'pictures_app/login.html')


def logout(request):
    request.session['user_id'] = None
    messages.error(request, "You have successfully logged out")
    return redirect('/login')
