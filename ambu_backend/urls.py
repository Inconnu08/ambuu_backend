"""
URL configuration for ambu_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.shortcuts import render
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from core.views import FirebaseDataViewSet
from medicine_orders.views import MedicineOrderViewSet


def render_react(request):
    return render(request, "../build/index.html")


router = DefaultRouter()
router.register(r'medicine-orders', MedicineOrderViewSet)
router.register('drivers', FirebaseDataViewSet, basename='drivers')

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^$", render_react),
    re_path(r"^(?:.*)/?$", render_react),
    path('api/v1/', include('core.api_urls')),
    path('api/v1/', include(router.urls)),
]
