from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("chat/<str:room_name>/", views.room, name="room"),
    path("chat/add_member",views.add_member_views, name="add_member"),
    path("chat/remove_member",views.remove_member_views, name="remove_member")
]