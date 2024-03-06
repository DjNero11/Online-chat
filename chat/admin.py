from django.contrib import admin

from .models import User, Room, Message
# Register your models here.

class RoomDataAdmin(admin.ModelAdmin):
    filter_horizontal = ("members",)

admin.site.register(User)
admin.site.register(Room, RoomDataAdmin)
admin.site.register(Message)