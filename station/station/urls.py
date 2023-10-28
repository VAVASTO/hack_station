from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('say_hello/', views.say_hello),
    path('get_map/', views.generate_map),
    path('set_position/', views.set_current_position),
    path('get_position/', views.get_current_coordinates),
    path('turn_autopilot_on/', views.start_update_coordinates)
]
