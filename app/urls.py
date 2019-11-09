from django.urls import path
from .views import ItemFilterView, ItemDetailView, ItemCreateView, ItemUpdateView, ItemDeleteView
from .views import Create_Account,Account_login,Some_view_1,Drivers_page,Users_page
from .views import Apro,Bpro,Cpro,Reserved,Choices,Kamase,MyCalendar,MonthWithScheduleCalendar

urlpatterns = [
    path('index/',  ItemFilterView.as_view(), name='index'),
    path('detail/<int:pk>/', ItemDetailView.as_view(), name='detail'),
    path('create/', ItemCreateView.as_view(), name='create'),
    path('update/<int:pk>/', ItemUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ItemDeleteView.as_view(), name='delete'),
    path('create_id/',Create_Account.as_view(),name='create_account'),
    path('login/',Account_login.as_view(),name='login'),
    path('signup/<int:pk>/',Some_view_1.as_view(),name='signup'),
    path('driversINFOforDRIVER/',Drivers_page.as_view(),name='driversINFOforDRIVER'),
    path('driversINFOforUSER/',Users_page.as_view(),name='driversINFOforUSER'),
    path('drivers_choice/',Choices.as_view(),name='drivers_choice'),
    path('kamasepage/',Kamase.as_view(),name='kamasepage'),
    #path('logout/',logout,{"template_name":"index.html"},name="logout"),
    path("logout/",Account_login.as_view(),name="logout"),
    path('Apro/',Apro.as_view(),name='Apro'),
    path("Bpro/",Bpro.as_view(),name="Bpro"),
    path("Cpro/<int:pk>/",Cpro.as_view(),name='Cpro'),
    path("reserved/",Reserved.as_view(),name="reserved"),
    path(
        'month_with_schedule/<int:year>/<int:month>/',
        MonthWithScheduleCalendar.as_view(), name='month_with_schedule'
    ),
    path(
        'mycalendar/<int:pk>/<int:year>/<int:month>/<int:day>/', MyCalendar.as_view(), name='mycalendar'
    ),
]
