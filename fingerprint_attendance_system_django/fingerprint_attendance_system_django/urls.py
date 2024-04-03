from django.contrib import admin
from django.urls import path
from fingerprint_attendance.views import index, enroll, verify

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('enroll/', enroll, name='enroll'),
    path('verify/', verify, name='verify'),
]
