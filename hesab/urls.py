from django.urls import path
from . import views
urlpatterns=[
    path('weeklist/', views.WeekList.as_view(), name='week_list'),
    path('<int:pk>/weekdetails/', views.week_details, name='week_details'),
    path('<int:pk>/refresh/', views.refresh, name='refresh'),
    path('<int:pk>/createmoney/', views.money_create_view, name='create_money'),
    path('<int:pk>/createshopping/', views.shopping_create_view, name='create_shopping'),
    path('<int:pk>/hesab/', views.hesab, name='hesab'),
    path('<int:pk>/lasthesabrefresh/', views.last_hesab_refresh, name='last_hesab_refresh'),
]