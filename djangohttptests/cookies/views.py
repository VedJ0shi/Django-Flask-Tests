from django.shortcuts import render, redirect
from .forms import CookieForm
import random, string

# Create your views here.
def cookie(request, any=None):
    '''functionality to ask server to set a cookie'''
    print('Cookies in incoming request:', request.COOKIES)
    context = {}
    if request.method == 'GET':
        context['form'] = CookieForm()
        if any:
            context['path'] = request.path
        return render(request, 'cookies/index.html', context)
    elif request.method == 'POST':
        form = CookieForm(request.POST)
        print('Raw request body:', request.body)
        print('Parsed request body:', request.POST)
        if form.is_valid():
            print('Client requests to set following cookie:', form.cleaned_data)
            cookie_name = f'cookie_{"".join(random.choices(string.ascii_uppercase, k=4))}'
            cookie_value = form.cleaned_data.get('random_str')
            max_age = form.cleaned_data.get('max_age')
            path = form.cleaned_data.get('path')
            if not path.endswith('cookies/'):
                cookie_name = cookie_name + f'_{path.split("/")[2]}'
            samesite = form.cleaned_data.get('samesite')
            httponly = form.cleaned_data.get('httponly')
            response = redirect(request.path) #redirects to current url
            response.set_cookie(key=cookie_name,
                                value=cookie_value,
                                max_age=max_age,  # Cookie expiration time in seconds
                                path=path,  # Path for which the cookie is valid
                                httponly=httponly,  # Prevent JavaScript access to the cookie
                                samesite=samesite)
            print(f'Success:{cookie_name} has been set on client')
            return response
        else:
            context['form'] = form
            return render(request, 'cookies/index.html', context )
        

