from __future__ import print_function, unicode_literals
from PyInquirer import print_function, prompt, print_json,style_from_dict,Token #unicode_literals, prompt, print_json,style_from_dict,Token
import argparse
import requests

#style = style_from_dict({
#    Token.Separator: '#cc5454',
#    Token.QuestionMark: '#673ab7 bold',
#    Token.Selected: '#cc5454',  # default
#    Token.Pointer: '#673ab7 bold',
#    Token.Instruction: '',  # default
#    Token.Answer: '#f44336 bold',
#    Token.Question: '',
#})


style = style_from_dict({
    Token.QuestionMark: 'FF9D00 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#5F891D bold',
    Token.Separator: '#cc5454',
    Token.QuestionMark: 'FF9D00 bold',
    Token.Selected: '',
    Token.Pointer: 'FF9D00 bold',
    Token.Instruction: '',  # default
    Token.Question: '',
})


class MyClient(object):
    def __init__(self, myclient):
        self.myclient = myclient

    def __init2__(self, myclient, professor_id, module_code):
        self.myclient = myclient
        self.professor_id=professor_id
        self.module_code = module_code

    def __init3__(self, myclient, professor_id, module_code, year, semester, rating):
        self.myclient = myclient
        self.professor_id = professor_id
        self.module_code = module_code
        self.year = year
        self.semester = semester
        self.rating = rating

    def register(self):
        print("Enter username, email and password (with a space in between each of them)")
    
    def login(self, url):
        source = self.myclient

    def logout(self):
        source = self.myclient


    def list(self):
        source = self.myclient
        print(source)
        if source:
            url = "http://127.0.0.1:8000/" + source
            call = requests.get(url)
            print('status:' call.status_code)
            response_data = call.json()

            module_list = response_data['modules']

        y=module_list
        for m in y:
            modules = {}
            result_m = {'Module Code': m['module_code'], 'Module Name': m['name'], 'year': m['year'], 'semester': m['semester']}
            modules.update(result_m)
            print(modules, "\n")
            return modules


    def view(self):
        source = self.myclient
        print(source)
        if source:
            url = "http://127.0.0.1:8000/" + source
            call = requests.get(url)
            print('status:' call.status_code)
            response_data = call.json()

            professor_list = response_data['professors']

        y = professor_list
        for p in y:
            professors = {}
            result_p = {'firstname': p['firstname'], 'lastname': p['lastname'], 'professor_id': p['professor_id'],
                        'rating': p['rating']}
            professors.update(result_p)
            print(professors, "\n")
            return professors

    def average(self, professor_id, module_code):
        source = self.myclient
        print(source)
        if source:
            url = "http://127.0.0.1:8000/" + source
            call = requests.get(url)
            print('status:'call.status_code)
            response_data = call.json()

            professor_list = response_data['professors']

            module_list = response_data['modules']

        y = professor_list
        for p in y:
            professors = {}
            result_p = {'firstname': p['firstname'], 'lastname': p['lastname'], 'professor_id': p['professor_id'],
                        'rating': p['rating']}
            result_m = {}
            professors.update(result_p)
            print(professors, "\n")
            return professors


    def rate(self, professor_id, module_code, year, semester, rating):
        source = self.myclient
        print(source)
        if source:
            url = "http://127.0.0.1:8000/" + source
            call = requests.get(url)
            print('status:' call.status_code)
            #response_data = call.json()


questions = [
        {
            'type': 'login',
        },
        {
            'type': 'register',
        },
        {
            'type': 'logout',
        },
        {
                'type': 'list',
        },
        {
            'type': 'view',
        },
        {
            'type': 'average',
        },
        {
            'type': 'rate',
        }
        ]


if __name__ == '__main__':
    #questions = [{}]
    response = prompt(questions, style=style)
    user_response = response['']
    user_response_obj=MyClient(user_response)

