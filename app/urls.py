from django.urls import path
from . import views


urlpatterns = [
    path('', view=views.homepage, name='home'),
    path('fruit-info', view=views.second_page, name='details_page'),
]