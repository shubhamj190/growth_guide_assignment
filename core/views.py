from django.forms import PasswordInput
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
import jwt
from growth_guide.settings import SECRET_KEY
from .utils import checking_admin_login
import os
import pandas as pd
import json
import urllib, mimetypes
from wsgiref.util import FileWrapper

# Create your views here.

def home_page(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        file_format= myfile.__dict__['_name'].split('.')[-1]
        if file_format not in  ['csv', 'xlsx']:
            messages.error(request, "please upload csv or xlsx files only !!" )
            return render(request, 'home_page.html')
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        messages.success(request, "file uploaded successfully!!" )
        return render(request, 'home_page.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'home_page.html')


def login_page(request):
    if request.method =="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username == "admin" and password == "admin":
            token=jwt.encode({"username": username, "password":password}, SECRET_KEY, algorithm="HS256")
            request.session['token']=token
            return HttpResponseRedirect('/dashboard')
        else:
            messages.error(request, "Please enter correct username and passwpord" )
            return render(request, 'login_page.html')

    return render(request, 'login_page.html')

def dashboard_page(request):
    is_authenticated=checking_admin_login(request)
    if not is_authenticated:
        return HttpResponseRedirect('/login')
    media_path = settings.MEDIA_ROOT
    file_list= os.listdir(media_path)
    context = {'files' : file_list, 'isloggedin':True}
    return render(request, 'dashboard_page.html', context)


def file_open(request, file_name):
    is_authenticated=checking_admin_login(request)
    if not is_authenticated:
        return HttpResponseRedirect('/login')
    file_format=file_name.split('.')[-1]
    media_path = settings.MEDIA_ROOT
    if file_format == "csv":
        df=pd.read_csv(media_path + '/'+ file_name)
        print(df)
    elif file_format =='xlsx':
        df=pd.read_excel(media_path + '/' + file_name)
    else:
        return HttpResponse("file format is incorrect")
    cols=[x for x in df.columns]
    json_records = df.reset_index().to_json(orient ='records')
    data = []
    data = json.loads(json_records)
    context={'cols':cols, 'd': data, 'isloggedin':True}

    return render(request, 'file_open.html', context)


def file_download(request, file_name):
    file_name = file_name
    file_path = settings.MEDIA_ROOT +'/'+ file_name
    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype )
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % str(file_name) 
    return response

def logout_admin(request):
    session=request.session
    del session['token']
    return HttpResponseRedirect('/login')