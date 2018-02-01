from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages



import bcrypt
from models import *


def index(request):
    if request=='POST':
        return redirect('/')
    else:
        return render(request, 'pictures_app/index.html', {"images": Image.objects.all()})

def renderForm(request):
    return render(request, 'pictures_app/upload.html')

def submitCriteria(request):
    Criteria.objects.create(name=request.POST['name'])
    return redirect('/upload')

def submitSubcategory(request):
    subcategory = Subcategory.objects.create(name=request.POST['name'])
    criteria = Criteria.objects.get(name=request.POST['criteria'])
    criteria.subcategories.add(subcategory)
    print subcategory
    return redirect('/upload')

def submitImage(request):
    print request.FILES['image']
    subcategory = Subcategory.objects.get(name=request.POST['subcategory'])
    image = Image.objects.create(image=request.FILES['image'], name=request.POST['name'])
    subcategory.images.add(image)

    return redirect('/upload')



def processRegistration(request):
    new_user = User.objects.user_validator(request.POST)
    print new_user
    if new_user[0] == True:
        messages.success(request, 'Welcome, ' + new_user[1].first_name)
        request.session['user_id'] = new_user[1].id
        return redirect('/quotes')
    else:
        for error in new_user[1]:
            messages.error(request, error)
        return redirect('/main')


def processLogin(request):
    this_user = User.objects.login_validator(request.POST)
    if this_user[0] == True:
        messages.success(request, 'Welcome, ' + this_user[1].first_name)
        request.session['user_id'] = this_user[1].id
        return redirect('/quotes')
    else:
        for error in this_user[1]:
            messages.error(request, error)
        return redirect('/main')


def showQuotes(request):
    if request.session['user_id']:
        quotes = Quote.objects.all().order_by('-created_at')
        print "********************", quotes
        this_user = User.objects.get(id=request.session['user_id'])
        print "FAVORITES", this_user.favorited_quotes.all()
        quotable_quotes = []
        for quote in quotes:
            favorited = False
            for user in quote.favorited_users.all():
                if user.id == request.session['user_id']:
                    favorited = True
            if favorited == False:
                quotable_quotes.append(quote)
        return render(request, 'quotes_app/quotes.html',
                {"quotes": quotable_quotes, "user": this_user,
                 "favorites": this_user.favorited_quotes.all()})
    else:
        return redirect('/main')

def submitQuote(request):

    errors = []
    if (len(request.POST['author']) < 3):
        errors.append("Quoted by: Must be more than 3 characters!")
    if (len(request.POST['quote']) < 10):
        errors.append("Quote must be more than 10 characters!")
    if len(errors) == 0:
        new_quote = Quote.objects.create(quote=request.POST['quote'],
                author=request.POST['author'])
        this_user = User.objects.get(id=request.session['user_id'])
        this_user.uploaded_quotes.add(new_quote)
        print this_user.uploaded_quotes.all()
        return redirect('/quotes')
    else:
        for error in errors:
            messages.error(request, error)
        return redirect('/quotes')




def logout(request):
    request.session['user_id'] = None
    messages.error(request, "You have successfully logged out")
    return redirect('/main')
