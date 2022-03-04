from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Sum
from django.contrib import auth
from .models import Student, Professor, Module, Rating
# Create your views here.
#this is server side
#def register(request):


def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active():
        #correct password and user is marked active
        auth.login(request, user)
        #redirect to a success page
        return HttpResponseRedirect("/index")
    else:
        #show error page
        return HttpResponseRedirect("/fault")

def logout(request):
    auth.logout(request)
    #redirect to success page
    return HttpResponseRedirect("/login")


def index(request):
    #return HttpResponse("<h1>MyClub Event Calendar</h1>")
    return render(request, 'index.html')

def fault(request):
    #return HttpResponse("<h1>MyClub Event Calendar</h1>")
    return render(request, 'fault.html')


#View a list of all module instances and the professor(s) teaching each of them
def list(request):
    modules = Module.objects.all()
    return render(request, 'events/module_list.html', {"modules": modules})


#View the rating of all professors
def view(request):
    # here make calculations for all the professors, getting their ratings from each module and computing average
    #do that by calling the ratings object
    professors = Professor.objects.all()
    for p in professors:
        ratings_sum = 0
        average = 0
        ratings = Rating.objects.filter(professor_id=p.professor_id)
        #now add those ratings
        for r in ratings:
            ratings_sum = ratings_sum + r.rating
        if p.ratings_count != 0:
            average = average + (ratings_sum/p.ratings_count)
            p.rating = average

    return render(request, 'events/professor_rating.html', {"professors": professors})


#View the average rating of a certain professor in a certain module
def average(request, professor_id, module_code): #need to make changes in path in urls.py to have that

    module = Module.objects.filter(module_code=module_code)
    #ratings = Rating.objects.filter(module_code=module_code, professor_id=professor_id)
    ratings = Rating.objects.filter(professor_id=professor_id)
    good_ratings = {}
    for x in ratings:
        if x.module_code == module_code:
            good_ratings |= x

    professor = Professor.objects.filter(professor_id=professor_id)
    rating_count = 1
    #rating_count = professor.ratings_count
    for p in professor:
        if p.professor_id==professor_id and p.ratings_count!=0:
            rating_count = p.ratings_count

    ratings_sum = 0
    for r in good_ratings:
        ratings_sum = ratings_sum + r.rating

    average_rating = ratings_sum/rating_count
    return render(request, 'events/professor_module_rating.html',
                  {"professor": professor, "average_rating": average_rating, "module": module})


#Rate the teaching of a certain professor in a certain module instance.
#this one I'm not sure about
#should be here? I think it should, since it goes from server side with calculations...
#tho from that side it could be that in rate.py, and from client side it would be in myclient.py stuff
def rate(request, professor_id, module_code, year, semester, rating): #same as above view function...hmmm do we need a form here? Or is it just client from command line

    professor = Professor.object.filter(professor_id=professor_id)
    module = Module.objects.filter(professor_id=professor_id, module_code=module_code, year=year, semester=semester)
    #Rating.objects.create(professor_id=request.data["professor_id"],
    #                      module_code=request.data["module_code"],
    #                      rating=request.data["rating"])
    Rating.objects.create(professor_id=request.data["professor_id"],
                          module_code=module_code,
                          rating=rating)

    professor.ratings_count = professor.ratings_count + 1
    return render(request, 'events/rate_professor.html')
#do we need a form it? maybe for client application part??? will get back to his for sure, since we ne
