from django.urls import path
from . import views
from . import classviews
import datetime


urlpatterns = [
    path('', classviews.BlogpostListView.as_view(), name="blog-home"), 
    path('post/<int:pk>/', classviews.BlogpostDetailView.as_view(), name = 'blog-post-x'),
    path('post/<int:pk>/update', classviews.BlogpostUpdateView.as_view(), name='blog-post-update'),
    path('post/<int:pk>/delete', classviews.BlogpostDeleteView.as_view(), name='blog-post-delete'),
    path('post/new/', classviews.BlogpostCreateView.as_view(), name ='blog-post-create'),
    path('about/', views.about, {"date": datetime.date.today()}, name="blog-about") #optional 3rd arg is keyword arg(s) passed to view function
]

'''
by default .as_view() considers the template path <appname>/<model>_<viewtype>.html
i.e. for first pattern, it will default to 'blog/blogpost_list.html'
'''