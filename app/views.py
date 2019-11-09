from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django_filters.views import FilterView

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.views.generic import CreateView, TemplateView,FormView
from . forms import UserCreateForm, LoginForm
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import HttpResponse
# from .predict import __predictor__

import numpy as np
from .filters import ItemFilter
from .forms import ItemForm
from .models import Item

import datetime
from django.views import generic
from .forms import BS4ScheduleForm, SimpleScheduleForm
from .models import Schedule
from . import mixins

# Create your views here.
# 検索一覧画面
class ItemFilterView(LoginRequiredMixin, FilterView):
    model = Item

    # デフォルトの並び順を新しい順とする
    queryset = Item.objects.all().order_by('-created_at')

    # django-filter用設定
    filterset_class = ItemFilter
    strict = False

    # 1ページあたりの表示件数
    paginate_by = 10

    # 検索条件をセッションに保存する
    def get(self, request, **kwargs):
        if request.GET:
            request.session['query'] = request.GET
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)

#ユーザ限定クラス
class UserOnlyMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser



# 詳細画面
class ItemDetailView(LoginRequiredMixin, DetailView):
    model = Item


# 登録画面
# class ItemCreateView(UserOnlyMixin, CreateView):
#     model = Item
#     form_class = ItemForm
#     template_name="signup.html"
#     def get_success_url(self):
#         return resolve_url('app:signup', pk=self.kwargs['pk'])

class ItemCreateView(LoginRequiredMixin, CreateView):
    # model = Item
    # form_class = ItemForm
    # template_name="signup.html"
    # #success_url = reverse_lazy('index')
    # def get_success_url(self):
    #     return resolve_url('app:create', pk=self.kwargs['pk'])
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')
     # def get_success_url(self):
     #     return resolve_url('app:update', pk=self.kwargs['pk'])

# 更新画面
class ItemUpdateView(UserOnlyMixin, UpdateView):
    model = Item
    form_class = ItemForm
    #template_name="signup.html"
    #success_url = reverse_lazy('index')
    def get_success_url(self):
        return resolve_url('app:update', pk=self.kwargs['pk'])

# 削除画面
class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Item
    success_url = reverse_lazy('index')


class Index(TemplateView):
    template_name = 'index.html'

index = Index.as_view()

#アカウント作成 (パスワードあり)
class Create_Account(CreateView):
    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            #フォームから'username'を読み取る
            username = form.cleaned_data.get('username')
            #フォームから'password1'を読み取る
            password = form.cleaned_data.get('password1')
            #フォームに入力された'username', 'password1'が一致する会員をDBから探し，userに代入
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/tpatch/create/')
        return render(request, 'create.html', {'form': form,})

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        return  render(request, 'create.html', {'form': form,})

#create_account = Create_Account.as_view()

#ログイン
class Account_login(View):
    def post(self, request, *arg, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('/tpatch/index')
            #return redirect('/tpatch/create/<int:pk>')
            #def get_success_url(self):
            #return redirect('app:update', pk=self.kwargs['pk'])
            #return redirect("app:update")
        return render(request, 'login.html', {'form': form,})

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        return render(request, 'login.html', {'form': form,})

#account_login = Account_login.as_view()

class Index_2(TemplateView):
    template_name = 'tpatch.html'

user = Index_2.as_view()



#ドライバー情報更新画面
class Some_view_1(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')

#ドライバー画面
class Drivers_page(TemplateView):
    def index(request):
        exchange_min=0.08970
        exchange_last=0.08978
        ab=np.array([[1,exchange_min,exchange_min*exchange_min,1,exchange_last,exchange_last*exchange_last]])
        val=__predictor__(ab)
        my_predict={
             "toku":val,
             }
        #template_name = 'driversINFOforDRIVER.html'
        return render(request,'driversINFOforDRIVER.html',my_predict)


#ドライバ情報のユーザー表示画面
class Users_page(TemplateView):
    template_name = 'driversINFOforUSER.html'

#driversINFOforUSER = Index_6.as_view()

class Choices(TemplateView):
    template_name = 'shiborikomi.html'
#drivers_choice = Index_7.as_view()
#
class Kamase(TemplateView):
    template_name = 'kamasepage.html'
#kamasepage = Index_8.as_view()

class Apro(TemplateView):
    template_name = 'driverAINFOforUSER.html'
#Apro = Apro.as_view()

class Bpro(TemplateView):
    template_name = 'driverBINFOforUSER.html'
#Bpro = Bpro.as_view()

# class Cpro(TemplateView):
#    template_name = 'driverCINFOforUSER.html'
from django.contrib.auth import get_user_model
User = get_user_model()
class Cpro(UserOnlyMixin,DetailView):
    model = Item
    form_class = ItemForm
    template_name="driverCINFOforUSER.html"
    #success_url = reverse_lazy('index')
    # def get_success_url(self):
    #      return resolve_url('app:Cpro', pk=self.kwargs['pk'])
         #return resolve_url('app:Cpro', pk=pk)
#Cpro = Cpro.as_view()

class Reserved(TemplateView):
    template_name = 'reserved.html'
#reserved = reserved.as_view()


class MyCalendar(UserOnlyMixin,mixins.MonthCalendarMixin, mixins.WeekWithScheduleMixin, CreateView):
    #"""月間カレンダー、週間カレンダー、スケジュール登録画面のある欲張りビュー"""
    template_name = 'app/mycalendar.html'
    model = Schedule
    date_field = 'date'
    form_class = BS4ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()
        context.update(week_calendar_context)
        context.update(month_calendar_context)
        return context

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        schedule = form.save(commit=False)
        schedule.date = date
        schedule.save()
        return redirect('mycalendar', year=date.year, month=date.month, day=date.day)


class MonthWithScheduleCalendar(mixins.MonthWithScheduleMixin, TemplateView):
    #"""スケジュール付きの月間カレンダーを表示するビュー"""
    template_name = 'app/month_with_schedule.html'
    model = Schedule
    date_field = 'date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context
