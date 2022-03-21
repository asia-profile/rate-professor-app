from django.shortcuts import render
import json
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.db.models import Sum
from django.contrib import auth
from .models import Student, Professor, Module, Rating
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
# Create your views here.
#this is server side


def proper_round(num, dec=0):
    num = str(num)[:str(num).index('.')+dec+2]
    if num[-1]>='5':
        return float(num[:-2-(not dec)]+str(int(num[-2-(not dec)])+1))
    return float(num[:-1])


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username') #get('uname')
        #email = request.POST.get('email')
        password = request.POST.get('password') #get('pwd')
        # print(uname, pwd)
        #if Student.objects.filter(username=username, email=email).count() > 0: #filter(username=uname)
        if Student.objects.filter(username=username).count() > 0:  # filter(username=uname)
            return HttpResponse('Username and/or email already exists.')
        else:
            user = Student(username=username, password=password) #, email=email) #user = Student(username=uname, password=pwd)
            user.save()
            return HttpResponse("/login")
    else:
        return HttpResponse("/fault")


def login(request, url):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password) #email=email, password=password)
        if user is not None and user.is_active():
        #correct password and user is marked active
            auth.login(request, user)
        #redirect to a success page
            return HttpResponseRedirect("/index")
        else:
        #show error page
            return HttpResponse("Faulty login/registration; try again")


def logout(request):
    auth.logout(request)
    #redirect to success page
    return HttpResponseRedirect("Logged out")


def index(request):
    return HttpResponse("<h1>Welcome to the site</h1>")
    #return render(request, 'index.html')


#View a list of all module instances and the professor(s) teaching each of them
def list(request): #seems to work, even if not elegant
    #in case of bad request
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content Type']  ='text/plain'
    if request.method!='GET':
        http_bad_response.content = 'Only GET requests allowed for this resource\n'

    #if reached here, then the request is good; get list of all modules from database
    modules = Module.objects.all().values('module_code', 'name', 'year', 'semester') #returns dictionary

    #collect objects and put them in new list items with appropriate json names
    list = []

    #have a queryset sth in
    for record in modules:
        #professors = record.professors.all().values('firstname', 'lastname', 'professor_id')
        module_professors = Module.objects.get(module_code=record['module_code'], year=record['year'], semester=record['semester']).\
            professors.all().values('firstname', 'lastname', 'professor_id')

        item = {'module_code': record['module_code'], 'module_name': record['name'], 'year': record['year'], 'semester': record['semester']} #, 'module_professors': record['professors']}

        list.append(item)
        for p in module_professors:
            item2 = {'firstname': p['firstname'], 'lastname': p['lastname'], 'professor_id': p['professor_id'],}
            list.append(item2)


    #make final json response payload
    payload = {'module list': list}
    #create and return normal response
    http_response = HttpResponse(json.dumps(payload))
    #http_response['Content Type'] = 'application/json'
    http_response.status_code = 200
    http_response.reason_phrase = 'OK'
    return http_response

    #modules = Module.objects.all()
    #return render(request, 'events/module_list.html', {"modules": modules})


#View the rating of all professors
def view(request): #bad numbers: JE gets 3 instead of 4, VS gets 2 instaed of 3; only TT gets as it should be 1
    #note: if I chanfe rating_sum at the beginning for 1 instad of 3 then we get good values for VS and TT
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content Type'] = 'text/plain'
    if request.method != 'GET':
        http_bad_response.content = 'Only GET requests allowed for this resource\n'

    # here make calculations for all the professors, getting their ratings from each module and computing average
    #do that by calling the ratings object

    professors_ids = Professor.objects.all().values('professor_id')
    for p in professors_ids:
        ratings_count=0
        ratings_sum = 0
        average = 0
        ratings = Rating.objects.filter(professor_id=p['professor_id'])
        #ratings = Rating.objects.filter(professor_id=p['professor_id']).values('rating')
        for r in ratings:
            ratings_sum = ratings_sum + r.rating
            #ratings_sum = ratings_sum + r['rating']
            ratings_count = ratings_count + 1
        average = (average + ratings_sum) / ratings_count
        average = proper_round(average, 0)
        #round(average) #okay, all is well, just doesn't round properly, gives 3 for 3,6666 and 2 for 2.5
        this_professor = Professor.objects.get(professor_id=p['professor_id'])
        this_professor.rating = average
        this_professor.save()


    #okay so now that we did the calculation for all the professors about their average - now only similar as in list ig
    # if reached here, then the request is good; get list of all professors from database
    professors = Professor.objects.all().values('firstname', 'lastname', 'professor_id', 'rating')
    # collect objects and put them in new list items with appropriate json names
    list = []
    for record in professors:
        item = {'firstname': record['firstname'], 'lastname': record['lastname'],
                'professor_id': record['professor_id'], 'rating': record['rating']}
        list.append(item)
        # make final json response payload
    payload = {'professor ranking list': list}

    # create and return normal response
    http_response = HttpResponse(json.dumps(payload))
    #http_response['Content Type'] = 'application/json'
    http_response.status_code = 200
    http_response.reason_phrase = 'OK'
    return http_response


#View the average rating of a certain professor in a certain module
def average(request, professor_id, module_code):

    ratings = Rating.objects.filter(professor_id=professor_id)
    ratings_count = 0
    ratings_sum = 0
    average = 0
    for r in ratings:
        ratings_sum = ratings_sum + r.rating
        # ratings_sum = ratings_sum + r['rating']
        ratings_count = ratings_count + 1

    average = (average + ratings_sum) / ratings_count
    average = proper_round(average, 0)

    this_professor = Professor.objects.get(professor_id=professor_id)
    this_professor.rating = average
    this_professor.save()


    # okay so now that we did the calculation for all the professors about their average - now only similar as in list ig
    # if reached here, then the request is good; get list of all professors from database
    # collect objects and put them in new list items with appropriate json names
    # make final json response payload

    list_p = []
    p = Professor.objects.filter(professor_id=professor_id).values('firstname', 'lastname', 'professor_id', 'rating')
    for record in p:
        item2 = {'module_code': module_code}
        item = {'firstname': record['firstname'], 'lastname': record['lastname'],
                'professor_id': record['professor_id'], 'has rating': record['rating']}

        list_p.append(item2)
        list_p.append(item)


    #create and return normal response
    payload = {'professor in module': list_p}
    http_response = HttpResponse(json.dumps(payload))
    #http_response['Content Type'] = 'application/json'
    http_response.status_code = 201
    http_response.reason_phrase = 'OK'
    return http_response


#Rate the teaching of a certain professor in a certain module instance.
def rate(request, professor_id, module_code, year, semester, rating): #same as above view function...hmmm do we need a form here? Or is it just client from command line


    #professor = Professor.objects.get(professor_id=professor_id)
    module = Module.objects.get(module_code=module_code, year=year, semester=semester)
    #Rating.objects.create(professor_id=request.data["professor_id"],
    #                      module_code=request.data["module_code"],
    #                      rating=request.data["rating"])
    new_rating = Rating.objects.create(module=module, professor_id=professor_id, rating=rating)
    
    data_rating = Rating.objects.filter(module=module, professor_id=professor_id, rating=rating).values('professor_id', 'rating')
    list_r = []
    for record in data_rating:
        #item2 = {'module_code': module_code}
        item = {'module_code': module_code, 'professor': record['professor_id'],
                'rating': record['rating']}

        #list_r.append(item2)
        list_r.append(item)



    payload = {'New rating created': list_r}
    http_response = HttpResponse(json.dumps(payload))
    #http_response['Content Type'] = 'application/json'
    http_response.status_code = 201
    http_response.reason_phrase = 'OK'
    return http_response
    #return render(request, 'events/rate_professor.html')
