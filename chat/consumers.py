import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


from .models import Message, Room
# created with help of Django channels documentation: https://channels.readthedocs.io/en/latest/

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        
        user = self.scope["user"]
        room_string = self.scope["url_route"]["kwargs"]["room_name"]
        room = Room.objects.get(room_name=room_string)
        m = Message.objects.create(room=room, sender=user,text=message)
        m.save()
    
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat.message", "message": message, "username": self.scope["user"].username }
        )

    
    def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        
        self.send(text_data=json.dumps({"message": message, "username": username }))