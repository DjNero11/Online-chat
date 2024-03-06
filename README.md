Distinctiveness and Complexity:
The distinctiveness of this project is that none of the previous CS50W projects were about real-time online text communication platform. My Online Chat is also based on WebSocket protocol for faster communication. For more reliable information transfer I used Redis with the use of docker which makes the process of stetting up Redis much easier. When it comes to complexity, Online Chat required understanding of WebSocket technology and its practical implementation. Online chat also has models about chat room, messages sent and users. Everything is created in such a way that users can log in, create room, send messages. Messages are transferred using WebSocket Protocol but in the meantime every message is saved in the database and is used to display chat history during next visit to chat room. Website is mobile responsive which can be seen in the video.

Files created or edited by me:
online_chat/urls.py: added chat/urls.py to be able to access app’s urls when the application is running.
Settings.py: Setings for Django project. Most created by Djnago during project creation. There are few settings added by me to allow WebSocket protocol transfer. 
asgi.py: Includes setting that allow WebSOcket protocol to work. 
Views.py: Takes care of http requests to the server. Index are settings for home page, room takes care of loading chat history when entering a chat room + makes sure user is authorised to enter the room, Add_member takes care of fetch API requests to add users to the chatroom, remove_member removes members form chatrooms, login and register take care of letting users into the website. 
Chat/urls.py: include all links used by chat app 
routing.py: Setting for WebSocket protocol 
Models.py: takes care of user, room and messages to be created in the database. Room is the „place” where messages are exchanges via WebSocket. Each room can have members, own name and id. Message model allows for saving of messages sent in the rooms. Each message has sender, room in which the message was sent, text and additionally timestamp and id.
Consumers.py: Gives much easier access to control WebSocket transfer than only using asgi.py. File was edited according to Django Channels recommendations with some changes done by me. File manages what happens during connection, disconnection and how messages are transferred to the other user in the same room as well as saves messages to database after message is sent. 
Admin.py: Allows easy database management via admin panel. 
Templates/chat: Include HTML templates for index, login, register and chat room page.
Static/chat: Include javascript.js which allows sending via websoctet protocol, Fetch API features and better user experience. Styles.css provides css styles to the website. 

Other files were created automatically by Django. 

How to run application: 
Install Docker
Open requirements.txt and install packages listed. 
Open docker
Open online_chat directory.
Run: „docker run --rm -p 6379:6379 redis:7”
Run: „python3 manage.py runserver”

