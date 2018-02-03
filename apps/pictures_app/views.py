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
        # images = []
        # criteria = Criteria.objects.order_by('?').first()
        # subcategories = random.sample(Subcategory.objects.filter(criteria=criteria),2)
        # images_3 = random.sample(Image.objects.filter(subcategory=subcategories[0]),3)
        # image_1 = random.sample(Image.objects.filter(subcategory=subcategories[1]),1)
        # if image_1[0].subcategory.name == "wild_animals":
        #     response = "Great Job! This is a wild animal, and other animals are domestic."
        # elif image_1[0].subcategory.name == "domestic_animals":
        #     response = "Great Job! This is a domestic animal, and other animals are wild."
        # elif image_1[0].subcategory.name == "in_flight":
        #     response = "Great Job! There is only one bird in flight, others are sitting on the branches."
        # elif image_1[0].subcategory.name == "not_in_flight":
        #     response = "Great Job! There is only one bird on the branch, others are flying."
        # elif image_1[0].subcategory.name == "one_animal":
        #     response = "Great Job! There is only one animal on this picture, and two animals on other pictures."
        # elif image_1[0].subcategory.name == "two_animals":
        #     response = "Great Job! There are two animals on this picture, and only one on other pictures."
        # elif image_1[0].subcategory.name == "one_bird":
        #     response = "Great Job! There is only one bird on this picture, and two birds on other pictures."
        # elif image_1[0].subcategory.name == "two_birds":
        #     response = "Great Job! There are two birds on this picture, and only one on other pictures."
        #
        # request.session['correct_answer'] = image_1[0].id
        # correct_answer = image_1[0].id
        #
        # images = images_3 + image_1
        # random.shuffle(images)
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
