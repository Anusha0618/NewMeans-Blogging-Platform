from django.conf.urls import url
from django.conf.urls.static import static


from blog.views.crud import *
from newmeans import settings
from django.urls import path

app_name = 'blog'

urlpatterns = [

path('create/',blogs_create ),
path('<int:pk>/',blogs_detail,name= "detail" ),
path('',blogs_list ),
path('<int:pk>/edit/',blogs_update,name = "update" ),
path('<int:pk>/delete/',blogs_delete ),
path('category/<str:spk>/',blogs_category ),


] + static(settings.STATIC_URL)
