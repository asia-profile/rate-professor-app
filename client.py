from __future__ import print_function, unicode_literals
import argparse
import sys
import requests
import json


def register(url):
    response = requests.get(url + 'register')
    print(json.dumps(response.json(), indent=1))


def login(url):
    response = requests.get(url + '/login')
    print(json.dumps(response.json(), indent=1))


def logut():
    response = requests.get('http://127.0.0.1:8000/logout')
    print(json.dumps(response.json(), indent=4))


def list():

    url = "http://127.0.0.1:8000/list"

    response = requests.get(url)
    print(json.dumps(response.json(), indent=1))


def view():

    url = "http://127.0.0.1:8000/view"

    response = requests.get(url)
    print(json.dumps(response.json(), indent=4))


def average(professor_id, module_code):
    url = "http://127.0.0.1:8000/" + professor_id + "/" + module_code + "/average"
    #json = requests.get(url).json()
    #print(json['average'])
    response = requests.get(url)
    print(json.dumps(response.json(), indent=4))


def rate(professor_id, module_code, year, semester, rating):
    url = 'http://127.0.0.1:8000/' + professor_id + "/" + module_code + "/" + year + "/" + semester + "/" + rating + "/rate"
    response = requests.get(url)
    print(json.dumps(response.json(), indent=1))


def main():
    command_line_argument = sys.argv
    #name client.py is taken as sys.argv[0]
    #name of command i.e. list, view, will be second one, and average and rate will be the last ones
    if command_line_argument[1] == "list":
        list()
    elif command_line_argument[1] == "view":
        view()
    elif command_line_argument[1] == "average":
        average(command_line_argument[2], command_line_argument[3])
    elif command_line_argument[1] == "rate":
        rate(command_line_argument[2], command_line_argument[3], command_line_argument[4], command_line_argument[5],
                command_line_argument[6])
    else:
        print("Not a supported command")


if __name__ == "__main__":
    main()
