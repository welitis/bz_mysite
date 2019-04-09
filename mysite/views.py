from django.shortcuts import render_to_response
from read_statistics.utils import *
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums, dates = get_seven_days_read_data(blog_content_type)
    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['sevenday_hot_data'] = get_7_days_hot_data(blog_content_type)
    return render_to_response('home.html', context)