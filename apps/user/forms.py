from django import forms
from django.contrib.auth import authenticate, login
from blog.models import User
from .models import OAuthRelationship


class LoginForm(forms.Form):
    username_or_email = forms.CharField(label='用户名或邮箱', label_suffix='', max_length=25, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入用户名或邮箱',
        'autofocus': 'autofocus',
    }))
    password = forms.CharField(label='密码', label_suffix='', max_length=16, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '请输入密码'
        }
    ))

    def clean(self):
        username_or_email = self.cleaned_data.get('username_or_email', '')
        password = self.cleaned_data.get('password', '')
        user = authenticate(username=username_or_email, password=password)
        if not user:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = authenticate(username=username, password=password)
                if user:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('就是不让你通过，哈哈哈')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=16, min_length=3, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入用户名',
        'id': 'username',
        'autofocus': 'autofocus',
        }
    ))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入邮箱'
        }
    ))
    verification_code = forms.CharField(label='验证码', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '点击"发送验证码"发送到邮箱',
    }))
    password = forms.CharField(label='密码', max_length=16, min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入密码',
        'id': 'password'
        }
    ))
    password_again = forms.CharField(label='确认密码', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '请再次确认密码'
        }
    ))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

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

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
            # 判断验证码
        code = self.request.session.get(self.clean_email())
        if code != verification_code:
            raise forms.ValidationError('验证码不正确')
        return verification_code


class ChangeNicknameForm(forms.Form):
    nickname_new = forms.CharField(label='新的昵称', label_suffix='', max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入新的昵称'
    }))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if hasattr(self, 'user'):
            if self.user.is_authenticated:
                self.cleaned_data['user'] = self.user
            else:
                raise forms.ValidationError('用户尚未登录')

    def clean_nickname_new(self):
        nickname_new = self.cleaned_data.get('nickname_new', '').strip()
        if nickname_new == '':
            raise forms.ValidationError('新的昵称不能为空')
        return nickname_new


class BindEmailForm(forms.Form):
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入正确的邮箱'
    }))
    verification_code =  forms.CharField(label='验证码', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '点击"发送验证码"发送到邮箱',
    }))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if hasattr(self, 'user'):
            if self.request.user.is_authenticated:
                self.cleaned_data['user'] = self.request.user
            else:
                raise forms.ValidationError('用户尚未登录')

        # 判断用户是否已绑定邮箱
        if self.request.user.email:
            raise forms.ValidationError('账户已绑定邮箱')
        return self.cleaned_data

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
            # 判断验证码
        code = self.request.session.get(self.clean_email())
        if code != verification_code:
            raise forms.ValidationError('验证码不正确')
        return verification_code

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已绑定账户')
        elif not email:
            raise forms.ValidationError("邮箱不能为空")
        return email


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='旧的密码', max_length=16, min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入旧密码',
        'id': 'old_password'
    }
    ))
    new_password = forms.CharField(label='新的密码', max_length=16, min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入新密码',
        'id': 'new_password'
    }
    ))
    new_password_again = forms.CharField(label='确认新的密码', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '请再次确认新密码'
    }
    ))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean(self):
        # 判断用户是否登录
        if hasattr(self, 'user'):
            if self.user.is_authenticated:
                self.cleaned_data['user'] = self.user
            else:
                raise forms.ValidationError('用户尚未登录')

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password', '').strip()
        if old_password == '':
            raise forms.ValidationError('密码不能为空')
        user = authenticate(username=self.user.username, password=old_password)
        if not user:
            raise forms.ValidationError("旧的密码不正确")
        return old_password

    def clean_new_password_again(self):
        new_password_again = self.cleaned_data.get('new_password_again')
        if new_password_again == '':
            raise forms.ValidationError('密码不能为空')
        password = self.cleaned_data.get('new_password')
        if password != new_password_again:
            raise forms.ValidationError('两次输入密码不一致')
        return new_password_again


class ForgotPasswordForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=16, min_length=3, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入用户名',
        'id': 'username',
        'autofocus': 'autofocus',
    }
    ))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入已绑定该用户的邮箱'
    }
    ))
    verification_code = forms.CharField(label='验证码', required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '点击"发送验证码"发送到邮箱',
    }))
    password = forms.CharField(label='新的密码', max_length=16, min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入新密码',
        'id': 'password'
    }
    ))
    password_again = forms.CharField(label='确认新密码', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': '请再次确认新密码'
    }
    ))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名不存在')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('用户未绑定该邮箱')
        return email

    def clean_password_again(self):
        password_again = self.cleaned_data.get('password_again')
        password = self.cleaned_data.get('password')
        if password != password_again:
            raise forms.ValidationError('两次输入密码不一致')
        return password_again

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
            # 判断验证码
        code = self.request.session.get(self.clean_email())
        if code != verification_code:
            raise forms.ValidationError('验证码不正确')
        return verification_code

    def clean(self):
        username = self.clean_username()
        email = self.clean_email()
        if not User.objects.filter(username=username, email=email).exists():
            raise forms.ValidationError("用户未绑定该邮箱")
        return self.cleaned_data


class BindQQForm(forms.Form):
    username_or_email = forms.CharField(label='用户名或邮箱', label_suffix='', max_length=25, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '请输入用户名或邮箱',
        'autofocus': 'autofocus',
    }))
    password = forms.CharField(label='密码', label_suffix='', max_length=16, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '请输入密码'
        }
    ))

    def clean(self):
        username_or_email = self.cleaned_data.get('username_or_email', '')
        password = self.cleaned_data.get('password', '')
        user = authenticate(username=username_or_email, password=password)
        if not user:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = authenticate(username=username, password=password)
                if user:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('就是不让你通过，哈哈哈')
        else:
            self.cleaned_data['user'] = user

        if OAuthRelationship.objects.filter(user=user, oauth_type=1).exists():
            raise forms.ValidationError("用户已绑定qq账号")
        return self.cleaned_data


