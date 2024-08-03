from django.shortcuts import render, HttpResponse

# Create your views here.
def visit(request):
    print('session_id inside incoming request:', request.COOKIES.get('sessionid'))
    print('User agent of client:', request.headers.get('User-Agent'))
    request.session['num_visits'] = request.session.get('num_visits', 0) + 1 #increment num_visits session variable
    return HttpResponse(f'Number of times you visited this page: {request.session["num_visits"]}')


