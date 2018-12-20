from django.contrib import admin
from django.urls import path
from reservationapp.views import NewRoom, ModifyRoom, delete_room, show_rooms, room, reservate, SearchRoom

urlpatterns = [
    path('admin/', admin.site.urls),
    path('room/new/', NewRoom.as_view(), name='new_room'),
    path('room/modify/<int:room_id>/', ModifyRoom.as_view(), name='modify_room'),
    path('room/delete/<int:room_id>/', delete_room, name='delete_room'),
    path('room/<int:room_id>', room, name='room'),
    path('adres/', show_rooms, name='adres'),
    path('reservation/<int:room_id>', reservate, name='reservate'),
    path('alert/', reservate, name='alert'),
    path('search/', SearchRoom.as_view(), name='search')
]
