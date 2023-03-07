
from django.contrib import admin
from django.urls import path
from core.views import home_page, login_page, dashboard_page, file_open, file_download, logout_admin

urlpatterns = [
    path('', home_page, name="home_page"),
    path('login/', login_page, name="login_page"),
    path('logout/', logout_admin, name="logout"),
    path('dashboard/', dashboard_page, name="login_page"),
    path('file-open/<str:file_name>', file_open, name="login_page"),
    path('download/<str:file_name>', file_download, name="login_page"),




]
