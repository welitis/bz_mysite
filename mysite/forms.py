from django import forms
from django.contrib.auth import authenticate, login
from blog.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', label_suffix='', max_length=15, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入用户名'
    }))
    password = forms.CharField(label='密码', label_suffix='', max_length=16, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '请输入密码'
        }
    ))

    def clean(self):
        username = self.cleaned_data.get('username', '')
        password = self.cleaned_data.get('password', '')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError('就是不让你通过，哈哈哈')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=16, min_length=3, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入用户名'
        }
    ))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入邮箱'
        }
    ))
    password = forms.CharField(label='密码', max_length=16, min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入密码'
        }
    ))
    password_again = forms.CharField(label='确认密码', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '请再次确认密码'
        }
    ))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password_again = self.cleaned_data.get('password_again')
        password = self.cleaned_data.get('password')
        if password != password_again:
            raise forms.ValidationError('两次输入密码不一致')
        return password_again



