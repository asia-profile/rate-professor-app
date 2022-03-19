from django.shortcuts import render
import json
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.db.models import Sum
from django.contrib import auth
from .models import Student, Professor, Module, Rating
# Create your views here.
#this is server side
#def register(request):

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username') #get('uname')
        email = request.POST.get('email')
        password = request.POST.get('password') #get('pwd')
        # print(uname, pwd)
        if Student.objects.filter(username=username, email=email).count() > 0: #filter(username=uname)
            return HttpResponse('Username and/or email already exists.')
        else:
            user = Student(username=username, password=password, email=email) #user = Student(username=uname, password=pwd)
            user.save()
            return HttpResponse("/login")
    else:
        return HttpResponse("/fault")


def login(request):
    username = request.POST.get('username', '')
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, email=email, password=password)
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
    return HttpResponse("<h1>Welcome to rating site</h1>")
    #return render(request, 'index.html')


def fault(request):
    return HttpResponse("<p>Faulty login/registration; try again</p>")
    #return render(request, 'fault.html')


#View a list of all module instances and the professor(s) teaching each of them
def list(request): #seems to work, even if not elegant
    #in case of bad request
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content Type']  ='text/plain'
    if request.method!='GET':
        http_bad_response.content = 'Only GET requests allowed for this resource\n'

    #if reached here, then the request is good; get list of all modules from database
    modules = Module.objects.all().values('module_code', 'name', 'year', 'semester', 'professors') #returns dictionary
    #professors = modules.values_list('professors')
    modules_queryset = Module.objects.all()
    for m in modules_queryset:
        professors = m.professors.all().values('firstname', 'lastname', 'professor_id')

    #collect objects and put them in new list items with appropriate json names
    list = []
    #have a queryset sth in

    for record in modules:
        #professors = record.professors.all().values('firstname', 'lastname', 'professor_id')

        item = {'module_code': record['module_code'], 'module_name': record['name'], 'year': record['year'],
                'semester': record['semester']} #, 'module_professors': record['professors']}
        item2 = {'Professor': professors[0]}

        #shows only id of professor or how many of professors are there or sth and we want to show a list of them
        list.append(item)
        list.append(item2)
        #okay now that works for display, even thou it' snot very elegant

    #list.append(modules.values_list('professors'))
    #make final json response payload
    payload = {'module list': list}
    #create and return normal response
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content Type'] = 'application/json'
    http_response.status_code = 200
    http_response.reason_phrase = 'OK'
    return http_response

    #modules = Module.objects.all()
    #return render(request, 'events/module_list.html', {"modules": modules})


#View the rating of all professors
def view(request): #seems to work, even if not elegant
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content Type'] = 'text/plain'
    if request.method != 'GET':
        http_bad_response.content = 'Only GET requests allowed for this resource\n'

    # here make calculations for all the professors, getting their ratings from each module and computing average
    #do that by calling the ratings object
    professors = Professor.objects.all()
    ratings_count = 0
    for p in professors:
        ratings_sum = 0
        average = 0
        ratings = Rating.objects.filter(professor_id=p.professor_id)
        #now add those ratings
        for r in ratings:
            ratings_sum = ratings_sum + r.rating
            ratings_count = ratings_count + 1
        if ratings_count != 0:
            average = average + (ratings_sum/ratings_count)
            p.rating = average
            p.save()
            #okay seem to work, since the rating for professor changed upon pulling up the url

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
    http_response['Content Type'] = 'application/json'
    http_response.status_code = 201
    http_response.reason_phrase = 'OK'
    return http_response

    #return render(request, 'events/professor_rating.html', {"professors": professors})


#View the average rating of a certain professor in a certain module
def average(request, professor_id, module_code):

    #module = Module.objects.filter(module_code=module_code)
    #ratings = Rating.objects.filter(module_code=module_code, professor_id=professor_id)
    ratings = Rating.objects.filter(professor_id=professor_id)
    good_ratings = {}
    how_many_ratings = 0
    for x in ratings:
        if x.module == module_code:
            good_ratings |= x
            how_many_ratings = how_many_ratings + 1

    #professor = Professor.objects.filter(professor_id=professor_id)
    #rating_count = 1
    #rating_count = professor.ratings_count
    #for p in professor:
    #    if p.professor_id==professor_id and p.ratings_count!=0:
    #        rating_count = p.ratings_count

    professor = Professor.objects.get(professor_id=professor_id)
    ratings_sum = 0
    #ratings_count = 0
    for r in good_ratings:
        ratings_sum = ratings_sum + r.rating
        #ratings_count = ratings_count + 1

    if how_many_ratings!=0:
        average_rating = ratings_sum/how_many_ratings
    else:
        average_rating = 1

    professor.rating = average_rating
    professor.save()
    # okay so now that we did the calculation for all the professors about their average - now only similar as in list ig
    # if reached here, then the request is good; get list of all professors from database
    # collect objects and put them in new list items with appropriate json names
    # make final json response payload

    list_p = []
    p = Professor.objects.filter(professor_id=professor_id).values('firstname', 'lastname', 'professor_id',
                                                                   'module', 'rating')
    for record in p:
        item = {'firstname': record['firstname'], 'lastname': record['lastname'],
                'professor_id': record['professor_id'], 'rating': record['rating']}
        item2 = {'module_code': module_code}

        list_p.append(item)
        list_p.append(item2)

    #create and return normal response
    payload = {'professor in module': list_p}
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content Type'] = 'application/json'
    http_response.status_code = 201
    http_response.reason_phrase = 'OK'
    return http_response
    #return render(request, 'events/professor_module_rating.html', {"professor": professor, "average_rating": average_rating, "module": module})


#Rate the teaching of a certain professor in a certain module instance.
#this one I'm not sure about
#should be here? I think it should, since it goes from server side with calculations...
#tho from that side it could be that in rate.py, and from client side it would be in myclient.py stuff
def rate(request, professor_id, module_code, year, semester, rating): #same as above view function...hmmm do we need a form here? Or is it just client from command line
    # okay, nowe ratings są dodawane - teraz tylko czy mamy zmieniany ich numer u profesora
    # wygląda na to, że chyba teraz jak coś poprawiłam to ratings count jest zmieniany

    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content Type'] = 'text/plain'
    if request.method != 'POST' or request.method != 'GET':
        http_bad_response.content = 'Only POST/GET requests allowed for this resource\n'


    professor = Professor.objects.get(professor_id=professor_id)
    module = Module.objects.get(module_code=module_code, year=year, semester=semester)
    #Rating.objects.create(professor_id=request.data["professor_id"],
    #                      module_code=request.data["module_code"],
    #                      rating=request.data["rating"])
    rating = Rating.objects.create(module=module, professor_id=professor_id, rating=rating)

    professor.save()

    #payload = {'New rating created': list_r}
    #http_response = HttpResponse(json.dumps(payload))
    http_response = HttpResponse()
    #http_response['Content Type'] = 'application/json'
    http_response.status_code = 201
    http_response.reason_phrase = 'OK'
    return http_response
    #return render(request, 'events/rate_professor.html')
