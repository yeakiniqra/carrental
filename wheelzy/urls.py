"""
URL configuration for wheelzy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rentcar.views import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('signup/', signup, name='signup'),
    path('ownersignup/', ownersignup, name = 'ownersignup'),
    path('user_profile/', user_profile, name='user_profile'),
    path('ownerprofile/', ownerprofile, name='ownerprofile'),
    path('ownerlogin/', ownerlogin, name='ownerlogin'),
    path('ownerlogout/', ownerlogout, name='ownerlogout'),
    path('booking_car/', booking_car, name='booking_car'),
    path('booking_review/<int:car_id>/<str:location>/<str:pickup_date>/<str:return_date>/', booking_review, name='booking_review'),
    path('upload_car/', upload_car, name='upload_car'),
    path('delete-car/<int:car_id>/', delete_car, name='delete_car'),
    path('owner_cars/', owner_cars, name='owner_cars'),
    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()