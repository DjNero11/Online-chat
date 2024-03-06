from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    id = models.AutoField(primary_key=True)

class Room(models.Model):
    id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=1000)
    members = models.ManyToManyField(User, related_name="members")

    def __str__(self):
        return self.room_name
    
class Message(models.Model):
    id = models.AutoField(primary_key=True)
    room = models.ForeignKey("Room", on_delete=models.CASCADE, related_name="message_room")
    sender = models.ForeignKey("User", on_delete=models.PROTECT, related_name="message_sender")
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=True)

    def __str__(self):
        return f"Message {self.id} in {self.room} from {self.sender}"