"""online_test_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include

from online_test_app import views

urlpatterns = [
    path('process-pdf/', views.upload_form,name="upload_form"),
    path('ans-sheet/', views.ans_sheet,name="ans_sheet"),
    path('quiz/', views.quiz,name="quiz"),
    path('quiz-clear/', views.quiz_clear,name="quiz-clear"),
    path('', views.upload_form)
]
