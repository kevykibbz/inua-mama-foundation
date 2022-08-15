from http.client import HTTPResponse
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.views.generic import View
from installation.models import SiteConstants
from .forms import *
from .decorators import unauthenticated_user,allowed_users
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
import re
from django.core.paginator import Paginator

# Create your views here.

class Application(View):
    def get(self,request):
        obj=SiteConstants.objects.count()
        if obj == 0:
            return redirect('/installation/')
        obj=SiteConstants.objects.all()[0]
        form=ApplicationForm()
        data={
            'title':f'Welcome to {obj.site_name}',
            'obj':obj,
            'data':request.user,
            'form':form,
        }
        return render(request,'manager/index.html',context=data)
    def post(self,request):
        form=ApplicationForm(request.POST,request.FILES or None)
        if form.is_valid():
            form.save()
            return JsonResponse({'valid':True,'message':'Application submitted successfully'},content_type="application/json")
        else:
            return JsonResponse({'valid':False,'uform_errors':form.errors},content_type="application/json")

#logout
def user_logout(request):
    logout(request)
    return redirect('/')



@method_decorator(unauthenticated_user,name='dispatch')
class UserAuth(View):
    def get(self,request):
        obj=SiteConstants.objects.count()
        if obj == 0:
            return redirect('/installation/')
        obj=SiteConstants.objects.all()[0]
        data={
            'title':'Login',
            'obj':obj
        }
        return render(request,'manager/login.html',context=data)
    def post(self,request):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            key=request.POST['username']
            password=request.POST['password']
            if key:
                if password:
                    regex=re.compile(r'([A-Za-z0-9+[.-_]])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
                    if re.fullmatch(regex,key):
                        #email address
                        if User.objects.filter(email=key).exists():
                            data=User.objects.get(email=key)
                            user=authenticate(username=data.username,password=password)
                        else:
                            form_errors={"username": ["Invalid email address."]}
                            return JsonResponse({'valid':False,'form_errors':form_errors},content_type="application/json")
                    else:
                        #username
                        if User.objects.filter(username=key).exists():
                            user=authenticate(username=key,password=password)
                        else:
                            form_errors={"username": ["Invalid username."]}
                            return JsonResponse({'valid':False,'form_errors':form_errors},content_type="application/json")
                        
                    if user is not None:
                        if 'remember' in request.POST:
                           request.session.set_expiry(1209600) #two weeeks
                        else:
                           request.session.set_expiry(0) 
                        login(request,user)
                        return JsonResponse({'valid':True,'feedback':'success:login successfully.'},content_type="application/json")
                    form_errors={"password": ["Password is incorrect or inactive account."]}
                    return JsonResponse({'valid':False,'form_errors':form_errors},content_type="application/json")
                else:
                    form_errors={"password": ["Password is required."]}
                    return JsonResponse({'valid':False,'form_errors':form_errors},content_type="application/json")
            else:
                form_errors={"username": ["Username is required."]}
                return JsonResponse({'valid':False,'form_errors':form_errors},content_type="application/json")


@login_required(login_url='/accounts/login')
@allowed_users(allowed_roles=['admins'])
def stats(request):
    obj=SiteConstants.objects.count()
    if obj == 0:
        return redirect('/installation/')
    obj=SiteConstants.objects.all()[0]
    data=ApplicationModel.objects.all().order_by('-id')
    paginator=Paginator(data,10)
    page_num=request.GET.get('page')
    applications=paginator.get_page(page_num)
    data={
        'title':'View Applications',
        'obj':obj,
        'data':request.user,
        'applications':applications,
        'count':paginator.count,
    }
    return render(request,'manager/stats.html',context=data)

