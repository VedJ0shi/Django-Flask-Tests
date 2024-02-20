from django.shortcuts import render
#from django.http import HttpResponse

posts =[
    {
        'author': 'Vedang',
        'title': 'First Post',
        'content': 'first post content...'
    },
    {
        'author': 'Spock',
        'title': 'Second Post',
        'content': 'second post content...'
    } ] #will be passed into a template as context variable


# Create your views here.
def home(request):
    #return HttpResponse('<h1>Blog Homepage</h1>')
    return render(request, 'blog/home.html', {'posts': posts}) #render still returns an HTTP Response

def about(request):
    #return HttpResponse('<h1>About this Blog</h1>')
    return render(request, 'blog/about.html')