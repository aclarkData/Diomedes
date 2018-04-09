# -*- coding: utf-8 -*-

import bottle
from bottle import route, run, template,static_file,error,request, auth_basic

# TODO get download info from Blueprint
# Make results page?

def check_creditionals(user,pw):
    username = "audit"
    password = "DirtyDigging"
    if pw == password and user == username:
        return True
    return False

@route('/')
@auth_basic(check_creditionals)
def home():
        return static_file('index.html', root='.')

@route('/query', method='POST')
@auth_basic(check_creditionals)
def main():
    company = request.POST.get('company')
    date = request.POST.get('date')

    # text clean
    #textToSummarize = textToSummarize.strip('')
    #textToSummarize = textToSummarize.encode('ascii', errors='ignore').decode()
    #ratio = float(ratio)


    return template('result',Summary=Summary)


@error(404)
@auth_basic(check_creditionals)
def error404(error):
    return template('error')

@error(405)
@auth_basic(check_creditionals)
def error405(error):
    return template('error')

@error(500)
@auth_basic(check_creditionals)
def error405(error):
    return template('error')


run(host='localhost', port=8000)
#run(host='0.0.0.0', port=80)
