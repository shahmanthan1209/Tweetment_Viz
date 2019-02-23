"""TweetMent URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from TweetMent.views import welcomePage,searchPage,resultPage,sigmaTest

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Tweetment/', welcomePage, name="Welcome_home"),
    path('Tweetment/searchPage', searchPage, name="search_page"),
    path('Tweetment/sigmaPage', sigmaTest, name="sigma_page"),
    path('Tweetment/result', resultPage, name="result_page"),
]
