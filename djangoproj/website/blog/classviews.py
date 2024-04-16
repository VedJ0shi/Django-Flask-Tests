from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *

class BlogpostListView(ListView):
    model = Blogpost #tells view which model to query
    template_name = 'blog/home.html' #overrides default template path
    context_object_name = 'posts'
    ordering = ['-last_modified'] #newest to oldest

    '''Since this inherits from ListView, it associates provided context name with the 
    object list/QuerySet of Blogpost model instances (passing it in as template variable)'''


class BlogpostDetailView(DetailView):
    model = Blogpost
    template_name = 'blog/post.html'
    context_object_name = 'post'

    '''associates context name with a single instance of the Blogpost model identified by
    primary key (DetailView expects 'pk' when called) passed in from the URLConf'''


class BlogpostCreateView(LoginRequiredMixin, CreateView): #view with a form
    model = Blogpost
    fields = ['title', 'content'] #set the Blogpost model fields to be handled by the form
    template_name = 'blog/form.html'
    success_url = '/blog/'
    

    def get_initial(self): #override inherited method (run automatically)
        initial = super().get_initial()
        initial['content'] = 'Please limit to 200 words'
        return initial #default dictionary that contains initial data for the form

    def form_valid(self, form:BaseModelForm): #override inherited method (run automatically)
        form.instance.author = self.request.user #author field in Blogpost model is correctly populated with current authenticated user
        return super().form_valid(form)


class BlogpostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): #view with a form
    model = Blogpost
    fields = ['title', 'content'] #set the Blogpost model fields to be handled by the form
    template_name = 'blog/form.html'
    success_url = '/blog/'

    def form_valid(self, form:BaseModelForm): #override inherited method (run automatically)
        form.instance.author = self.request.user #author field in Blogpost model is correctly populated with current authenticated user
        return super().form_valid(form)
    
    def test_func(self): #checks if current user is indeed te author of post being updated
        current_post = self.get_object() #.get_object() is an inherited method that returns current model instance
        if self.request.user == current_post.author:
            return True
        return False
    
    '''retrieves Blogpost model instance to update identified by
    primary key (UpdateView expects 'pk' when called) passed in from the URLConf '''


class BlogpostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Blogpost
    template_name = 'blog/delete.html'
    context_object_name = 'post'
    success_url = '/blog/'

    def test_func(self): #checks if current user is indeed te author of post being updated
        current_post = self.get_object() #.get_object() is an inherited method that returns current model instance
        if self.request.user == current_post.author:
            return True
        return False