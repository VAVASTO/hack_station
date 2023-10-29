from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('say_hello/', views.say_hello),
    path('get_map/', views.generate_map),
    path('set_position/', views.set_current_position),
    path('get_position/', views.get_current_coordinates),
    path('break_something/', views.break_something),
    path('get_broken_detail/', views.get_broken_detail),
    path('get_details/', views.get_details),
    path('get/wheels/', views.get_wheels),
    path('get/panels/', views.get_solar_panel),
    path('get/others/', views.get_other)
]
