from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('', views.index, name='index'),
    path('list', views.list, name='list'),
    path('view', views.view, name='view'),
    path('<str:professor_id>/<str:module_code>/average', views.average, name='average'),
    path('<str:professor_id>/<str:module_code>/<int:year>/<int:semester>/<int:rating>/rate', views.rate, name='rate'),
  ]