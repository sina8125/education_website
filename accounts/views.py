# Django
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.conf import settings

# local
from .forms import UserRegistrationForm, VerifyPhoneNumberForm, UserLoginForm, ChangePasswordForm, UserChangeForm
from .models import OtpCode, User
from .serializer import LoginSerializer, RegisterSerializer, VerifyCodeSerializer

# python
import datetime
import random

# third package
from kavenegar import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import RefreshToken, Token, AccessToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed
from rest_framework import status


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('API KEY')
        params = {
            'sender': '',
            'receptor': str(phone_number).replace(' ', ''),
            'message': _(f'کد تایید شما:\n'
                         f'{code}')
        }
        response = api.sms_send(params)
    except Exception as e:
        print(e)
        raise e


class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register.html',
                      context={'register_form': UserRegistrationForm})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            birthday = form.cleaned_data['birthday'].isoformat() if form.cleaned_data['birthday'] else None
            request.session['user_info'] = {
                'phone_number': str(form.cleaned_data['phone_number']),
                'email': form.cleaned_data['email'],
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'birthday': birthday,
                'password': form.cleaned_data['password2'],
            }

            random_code = random.randint(1000, 9999)
            otp_instance, created = OtpCode.objects.get_or_create(phone_number=form.cleaned_data['phone_number'],
                                                                  created_time__gt=timezone.now() - timezone.timedelta(
                                                                      minutes=2),
                                                                  defaults={
                                                                      'code': random_code
                                                                  })
            if not created:
                random_code = otp_instance.code
            # try:
            #     send_otp_code(form.cleaned_data['phone_number'], random_code)
            # except Exception as e:
            #     messages.error(request, _('ارسال کد با مشکل مواجه شد'), 'danger')
            #     return render(request, 'accounts/register.html', {'register_form': form})

            messages.success(request, _('کد تایید ارسال شد'), 'success')
            return redirect('accounts:verify_code')
        return render(request, 'accounts/register.html', {'register_form': form})


class VerifyCodeView(View):
    def get(self, request):
        return render(request, 'accounts/verify.html', {'verify_form': VerifyPhoneNumberForm})

    def post(self, request):
        user_info = request.session['user_info']
        previous_phone_number = user_info.get('previous_phone_number', None)
        phone_number = user_info['phone_number']
        email = user_info['email']
        first_name = user_info['first_name']
        last_name = user_info['last_name']
        birthday = datetime.date.fromisoformat(user_info['birthday']) if user_info['birthday'] else None
        password = user_info['password']
        code_instance = get_object_or_404(OtpCode, phone_number=phone_number,
                                          created_time__gt=timezone.now() - timezone.timedelta(minutes=2))
        form = VerifyPhoneNumberForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                if previous_phone_number:
                    user = User.objects.get(phone_number=previous_phone_number)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.email = email
                    user.birthday = birthday
                    user.phone_number = phone_number
                    user.save()
                    request.session['user_info']['previous_phone_number'] = phone_number
                    messages.success(request, _('تغییرات با موفقیت ثبت شد'), 'success')
                    return redirect('accounts:profile:information')
                else:
                    User.objects.create_user(phone_number=phone_number, email=email, first_name=first_name,
                                             last_name=last_name, birthday=birthday, password=password)
                    messages.success(request, _('ثبت نام با موفقیت انجام شد'), 'success')
                    return redirect('accounts:login')
            else:
                messages.error(request, _('کد تایید نادرست است'), 'danger')
                return redirect('accounts:verify_code')
        return render(request, 'accounts/verify.html', {'verify_form': form})


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html', {'login_form': UserLoginForm})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, _('با موفقیت وارد شدید'), 'info')
                return redirect('post:home:post-list')
            messages.error(request, _('شماره موبایل یا پسورد نادرست است'), 'danger')
        return render(request, 'accounts/login.html', {'login_form': form})


class ProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'accounts/profile.html', {'form': UserChangeForm(instance=request.user)})

    @method_decorator(login_required)
    def post(self, request):
        user = User.objects.get(pk=request.user.pk)
        form = UserChangeForm(request.POST, instance=user)
        if form.is_valid():
            if 'phone_number' in form.changed_data:
                birthday = form.cleaned_data['birthday'].isoformat() if form.cleaned_data['birthday'] else None
                request.session['user_info'] = {
                    'previous_phone_number': str(request.user.phone_number),
                    'phone_number': str(form.cleaned_data['phone_number']),
                    'email': form.cleaned_data['email'],
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'birthday': birthday,
                    'password': form.cleaned_data['password'],
                }
                random_code = random.randint(1000, 9999)
                otp_instance, created = OtpCode.objects.get_or_create(phone_number=form.cleaned_data['phone_number'],
                                                                      created_time__gt=timezone.now() - timezone.timedelta(
                                                                          minutes=2),
                                                                      defaults={
                                                                          'code': random_code
                                                                      })
                if not created:
                    random_code = otp_instance.code
                # try:
                #     send_otp_code(form.cleaned_data['phone_number'], random_code)
                # except Exception as e:
                #     messages.error(request, _('ارسال کد با مشکل مواجه شد'), 'danger')
                #     return render(request, 'accounts/profile.html', {'form': form})
                messages.success(request, _('کد تایید ارسال شد'), 'success')
                return redirect('accounts:verify_code')
            else:
                form.save()
                messages.success(request, _('تغییرات اعمال شد'), 'success')
                return redirect('accounts:profile:information')
        return render(request, 'accounts/profile.html', {'form': form})


class ChangePasswordView(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'accounts/change_password.html', context={'form': ChangePasswordForm})

    @method_decorator(login_required)
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            form = ChangePasswordForm(user, request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                password = cd['password2']
                user.set_password(password)
                user.save()
                messages.success(request, _('رمز عبور شما تغییر کرد\nلطفا مجدد وارد شوید'), 'success')
                return redirect('post:home:post-list')
            return render(request, 'accounts/change_password.html', {'form': form})
        messages.error(request, _('برای تغییر رمز ابتدا وارد شوید'), 'danger')
        return redirect('post:home:post-list')


class ProfileSubscriptionView(View):
    @method_decorator(login_required)
    def get(self, request):
        user = request.user
        subscriptions = user.subscriptions.filter(expire_time__gt=timezone.now()).order_by('-expire_time')
        if subscriptions.exists():
            subscriptions = subscriptions[0]
            remaining_time = _("{days} روز و {H} ساعت و {M} دقیقه").format(days=subscriptions.remaining_time.days,
                                                                           H=(
                                                                                   subscriptions.remaining_time.seconds // 3600),
                                                                           M=(
                                                                                     subscriptions.remaining_time.seconds % 3600) // 60)
            return render(request, 'accounts/profile_subscription.html', {'remaining': remaining_time})
        else:
            return render(request, 'accounts/profile_subscription.html')


class UserLogoutView(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        messages.success(request, _('خروج با موفقیت انجام شد'), 'success')
        return redirect('post:home:post-list')


# ----------------------------
# api

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def set_token_cookie(response, access=None, refresh=None):
    if access:
        access = AccessToken(access)
        response.set_cookie('access_token',
                            str(access),
                            expires=timezone.now() + access.lifetime,
                            secure=settings.SESSION_COOKIE_SECURE,
                            httponly=True
                            )
    if refresh:
        refresh = RefreshToken(refresh)
        response.set_cookie('refresh_token',
                            str(refresh),
                            expires=timezone.now() + refresh.lifetime,
                            secure=settings.SESSION_COOKIE_SECURE,
                            httponly=True
                            )
    return response


class RefreshTokenView(TokenRefreshView):
    def post(self, request: Request, *args, **kwargs):
        data = {'refresh': str(request.COOKIES.get('refresh_token'))}
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        response = Response({'detail': _('توکن جدید ایجاد شد')})
        response = set_token_cookie(response, **serializer.validated_data)
        return response


class LoginAPIView(APIView):
    def post(self, request: Request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.data.get('phone_number')
        password = serializer.data.get('password')
        user = authenticate(phone_number=phone_number, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            response = Response({'phone_number': phone_number})
            response = set_token_cookie(response, **token)
            print(response.cookies)
            return response
        else:
            raise AuthenticationFailed(detail=_('شماره تلفن یا پسورد نادرست است'), code='data_incorrect')


class RegisterAPIView(APIView):
    def post(self, request: Request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        birthday = serializer.validated_data['birthday'].isoformat() if serializer.validated_data.get(
            'birthday') else None
        request.session['user_info'] = {
            'phone_number': str(serializer.validated_data['phone_number']),
            'email': serializer.validated_data.get('email', None),
            'first_name': serializer.validated_data['first_name'],
            'last_name': serializer.validated_data.get('last_name', ''),
            'birthday': birthday,
            'password': serializer.validated_data['password'],
        }
        random_code = random.randint(1000, 9999)
        otp_instance, created = OtpCode.objects.get_or_create(
            phone_number=serializer.validated_data.get('phone_number'),
            created_time__gt=timezone.now() - timezone.timedelta(
                minutes=2),
            defaults={
                'code': random_code
            })
        if not created:
            random_code = otp_instance.code
        # try:
        #     send_otp_code(str(serializer.validated_data['phone_number']), random_code)
        # except Exception as e:
        #     raise AuthenticationFailed(_('ارسال کد با مشکل مواجه شد'), code='send_code_failed')
        return Response({'detail':_('کد تایید ارسال شد')}, status=status.HTTP_200_OK)


class VerifyCodeAPIView(APIView):
    def post(self, request: Request):
        validated_data = request.session.get('user_info')
        birthday = datetime.date.fromisoformat(validated_data['birthday']) if validated_data.get('birthday') else None
        validated_data['birthday'] = birthday
        data = request.data
        data['phone_number'] = validated_data.get('phone_number')
        serializer = VerifyCodeSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        code_instance = OtpCode.objects.get(phone_number=validated_data.get('phone_number'),
                                            created_time__gt=timezone.now() - timezone.timedelta(minutes=2))
        if serializer.validated_data['code'] == code_instance.code:
            User.objects.create_user(**validated_data)
            serializer.save()
            return Response({'detail':_('ثبت نام با موفقیت انجام شد')},status=status.HTTP_201_CREATED)
        else:
            raise AuthenticationFailed(_('کد تایید نادرست است'),code='verify_code_incorrect')
