import datetime

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import authenticate, login

from blog.models import Blog
from read_statistics.utils import *
from .forms import RegForm, LoginForm


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date)\
        .values('id', 'title').annotate(read_num_sum=Sum('read_details__read_num'))\
        .order_by('-read_num_sum')
    return blogs[:7]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    read_nums, dates = get_seven_days_read_data(blog_content_type)

    # 获取7天热门博客的缓存数据
    sevenday_hot_data = cache.get('sevenday_hot_data')
    if sevenday_hot_data is None:
        sevenday_hot_data = get_7_days_hot_blogs()
        cache.set('sevenday_hot_data', sevenday_hot_data, 3600)

    context = {}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['sevenday_hot_data'] = sevenday_hot_data
    return render(request, 'home.html', context)


def login_views(request):
    context = {}
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data.get('user')
            login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        login_form = LoginForm()
    context['login_form'] = login_form
    return render(request, 'login.html', context)


def register_views(request):
    context = {}
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data.get('username')
            password = reg_form.cleaned_data.get('password')
            email = reg_form.cleaned_data.get('email')
            User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            # 登录用户
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(request.GET.get('from', reverse('home')))

    else:
        reg_form = RegForm()
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)
