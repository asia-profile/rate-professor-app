from __future__ import print_function, unicode_literals
import argparse
import sys
import requests
import click

cli = click.Group()

@cli.command()
def register():
    json = requests.get('http://127.0.0.1:8000/register').json()
    print(json['register'])


@cli.command()
def login(url):
    json = requests.get(url).json()
    print(json['login'])


@cli.command()
def logut():
    json = requests.get('http://127.0.0.1:8000/logout').json()
    print(json['logout'])


@cli.command()
def list():
    json = requests.get('http://127.0.0.1:8000/list').json()
    print(json['list'])


@cli.command()
def view():
    json = requests.get('http://127.0.0.1:8000/view').json()
    print(json['view'])


#think need to change a bit here, since we're to get that all from command line, so maybe story the *args somewhere
@cli.command()
def average(professor_id, module_code):
    url = 'http://127.0.0.1:8000/' + professor_id + '/' + module_code + '/average'
    json = requests.get(url).json()
    print(json['average'])


@cli.command()
def rate(professor_id, module_code, year, semester, rating):
    url = 'http://127.0.0.1:8000/' + professor_id + '/' + module_code + '/' + year + '/' + semester + '/' + rating + '/rate'
    json = requests.get(url).json()
    print(json['rate'])


@cli.command()
#@cli.argument("namespace", nargs=1)
def process(namespace):
    print("x")

@cli.command()
def run(ctx):
    #for namespace in KEYS.iterkeys():
    #    ctx.invoke(process, namespace=namespace)
    for command in sys.argv:
        if command=="list":
            ctx.invoke(list)
        if command=="view":
            ctx.invoke(view)



#@click.command()
#def main():
#    command_line_argument = sys.argv
    #name client.py is taken as sys.argv[0]
    #name of command i.e. list, view, will be second one, and average and rate will be the last ones
#    print(command_line_argument)
#    if command_line_argument[1] == "list":
#        list()
#    if command_line_argument[1] == "view":
#        view()
#    if command_line_argument[1] == "average":
#        average(command_line_argument[2], command_line_argument[3])
#    if command_line_argument[1] == "rate":
#        rate(command_line_argument[2], command_line_argument[3], command_line_argument[4], command_line_argument[5],
#                command_line_argument[6])
#    else:
#        print("Not a supported command")


#if __name__ == "__main__":
#    main()
