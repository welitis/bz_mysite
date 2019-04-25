import string
import random
import time
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

from .forms import RegForm, LoginForm, ChangeNicknameForm, BindEmailForm, ChangePasswordForm, ForgotPasswordForm
from .models import Profile


from django.shortcuts import render

# Create your views here.


def login_views(request):
    context = {}
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data.get('user')
            login(request, user)
            return redirect(request.POST.get('from', reverse('home')))
        else:
            context['from'] = request.POST.get('from', reverse('home'))
    else:
        login_form = LoginForm()
    context['login_form'] = login_form
    context.setdefault('from', request.GET.get('from', reverse('home')))
    return render(request, 'user/login.html', context)


def login_for_medal(request):
    context = {}
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data.get('user')
            login(request, user)
            context['status'] = 'success'
        else:
            context['status'] = 'error'
    else:
        context['status'] = 'error'
    return JsonResponse(context)


def register_views(request):
    context = {}
    if request.method == 'POST':
        reg_form = RegForm(request.POST, request=request)
        if reg_form.is_valid():
            username = reg_form.cleaned_data.get('username')
            password = reg_form.cleaned_data.get('password')
            email = reg_form.cleaned_data.get('email')
            User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            # 清除session
            del request.session[email]
            # 登录用户
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(request.POST.get('from', reverse('home')))
        else:
            context['from'] = request.POST.get('from', reverse('home'))
    else:
        reg_form = RegForm()
    context['reg_form'] = reg_form
    context.setdefault('from', request.GET.get('from', reverse('home')))
    return render(request, 'user/register.html', context)


def logout_views(request):
    logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def user_info(request):
    context = {}
    return render(request, 'user/personal_info.html', context)


def change_nickname(request):
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data.get('nickname_new')
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()  # 修改昵称完成
            return redirect(reverse('user_info'))
    elif request.method == 'GET':
        form = ChangeNicknameForm()
    else:
        return JsonResponse({'status': 'error', 'code': 403})

    context = {}
    context['form'] = form
    context['page_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['form_title'] = '修改昵称'
    context['return_back_url'] = reverse('user_info')
    return render(request, 'user/change_nickname.html', context)


def bind_email(request):
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 清除session
            del request.session[email]
            return redirect(reverse('user_info'))
    elif request.method == 'GET':
        form = BindEmailForm()
    else:
        return JsonResponse({'status': 'error', 'code': 403})

    context = {}
    context['form'] = form
    context['page_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form_title'] = '绑定邮箱'
    context['return_back_url'] = reverse('user_info')
    return render(request, 'user/bind_email.html', context)


def send_verify_code(request):
    email = request.GET.get('email', '')
    data = {}
    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters+string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'error'
            data['message'] = '发送邮件过于频繁，请稍后再试'
        elif User.objects.filter(email=email).exists():
            if request.GET.get('send_for', '') == 'reset_password':
                request.session[email] = code
                request.session['send_code_time'] = now
                send_mail(
                    '重置密码',
                    '验证码：' + str(code),
                    '943446906@qq.com',
                    [email],
                    fail_silently=False,
                )
                data['status'] = 'success'
            else:
                data['status'] = 'error'
                data['message'] = '该邮箱已绑定账户'
        else:
            request.session[email] = code
            request.session['send_code_time'] = now
            send_mail(
                '绑定邮箱',
                '验证码：'+ str(code),
                '943446906@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'success'
    else:
        data['status'] = 'error'
        data['message'] = '邮箱地址不正确'
    return JsonResponse(data)


def ajax_confirm(request):
    data = {}
    if request.is_ajax():
        if request.method == "GET":
            username = request.GET.get('username')
            if User.objects.filter(username=username).exists():
                data['status'] = 0
                return JsonResponse(data)
    data['status'] = 1
    return JsonResponse(data)


def cancel_email(request):
    data = {}
    if request.is_ajax():
        if request.method == "GET":
            user = request.user
            if user.is_authenticated:
                user.email = ''
                user.save()
                data['status'] = 'success'
                return JsonResponse(data)
    data['status'] = 'error'
    return JsonResponse(data)


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            new_password = form.cleaned_data.get('new_password')
            user = request.user
            user.set_password(new_password)
            user.save() # 修改密码成功
            logout(request)
            return redirect(reverse('user_info'))
    elif request.method == 'GET':
        form = ChangePasswordForm()
    else:
        return JsonResponse({'status': 'error', 'code': 403})

    context = {}
    context['form'] = form
    context['page_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form_title'] = '修改密码'
    context['return_back_url'] = reverse('user_info')
    return render(request, 'user/change_password.html', context)


def forgot_password(request):
    context = {}
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            # 清除session
            del request.session[email]
            return redirect(request.POST.get('from',reverse('home')))
        else:
            context['from'] = request.POST.get('from', reverse('home'))
    elif request.method == 'GET':
        form = ForgotPasswordForm()
    else:
        return JsonResponse({'status': 'error', 'code': 403})

    context['form'] = form
    context['keep_status'] = 1
    context['page_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['form_title'] = '重置密码'
    context.setdefault('return_back_url', request.GET.get('from', reverse('home')))
    return render(request, 'user/forgot_password.html', context)