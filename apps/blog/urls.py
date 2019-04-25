from django.urls import path
from .views import *

app_name = 'blog'
urlpatterns = [
    path('', blog_list, name="blog_list"),
    path('<int:blog_pk>', blog_detail, name="blog_detail"),
    path('type<int:blog_type_pk>', blog_type_list, name="blog_type_list"),
    path('date/<int:year>/<int:month>', blog_date_list, name="blog_date_list"),
]