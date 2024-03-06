from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required

from .models import User, Room, Message

@login_required(login_url="login")
def index(request):
    if request.method == "POST":
        user = request.user
        new_room_name = request.POST["index_create_room"]

        new_room = Room.objects.create(room_name=new_room_name)
        new_room.members.add(user)
        new_room.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        user = request.user
        user_rooms = Room.objects.filter(members=user)

        return render(request, "chat/index.html", {"user_rooms":user_rooms})

@login_required(login_url="login")
def room(request, room_name):
    user = request.user
    try:
        room = Room.objects.get(room_name=room_name)
    except:
        return HttpResponse("No room with this name.")
    
    if user not in room.members.all():
        return HttpResponse("No access to this room.")
    else:
        messages = Message.objects.filter(room=room)
        room_members = room.members.all()
        return render(request, "chat/room.html", {"room_name": room_name, "user_views":user.username, "messages": messages, "room_members":room_members })

@login_required(login_url="login")
def add_member_views(request):
    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)
        new_member = data.get("new_member")
        room_too_add_user = data.get("room")
        if not user.is_authenticated:
            return JsonResponse({
                "Error": "User not signed in "
            }, status=400)
        else:
            try:
                current_room = Room.objects.get(room_name=room_too_add_user)
                if user not in current_room.members.all():
                    return JsonResponse({
                    "error": "Error with room."
                    }, status=400)
            except:
                return JsonResponse({
                "error": "Error with room."
                }, status=400)
            try:
                new_member_object = User.objects.get(username=new_member)
            except:
                return JsonResponse({
                "error": "User does not exist."
                }, status=400)
            
            current_room.members.add(new_member_object)
            return JsonResponse({
                "Message": "Success",
                "user_id": new_member_object.id,
                "remove_path": reverse("remove_member"),
                "room_name":room_too_add_user

            }, status=201)  
    else:
        return JsonResponse({
            "error": "Post method request required."
        }, status=400)

@login_required(login_url="login")
def remove_member_views(request):
    if request.method == "POST":
        user = request.user
        data = json.loads(request.body)

        user_id_to__remove = data.get("user_id")
        room = data.get("room")

        if not user.is_authenticated:
            return JsonResponse({
                "Error": "User not signed in "
            }, status=400)
        else:
            try:
                current_room = Room.objects.get(room_name=room)
                if user not in current_room.members.all():
                    return JsonResponse({
                    "error": "Error with room."
                    }, status=400)
            except:
                return JsonResponse({
                "error": "Error with room."
                }, status=400)
            try:
                new_member_object = User.objects.get(id=user_id_to__remove)
            except:
                return JsonResponse({
                "error": "User does not exist."
                }, status=400)
            
            current_room.members.remove(new_member_object)
            return JsonResponse({
                "Message": "Success",
            }, status=201)  

    else:
        return JsonResponse({
            "error": "Post method request required."
        }, status=400)

#based on default login requiterments created by cs50 in previous projects:
def login_view(request):
    if request.method == "POST":

        
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "chat/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "chat/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

#based on default register requiterments created by cs50 in previous projects:
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "chat/register.html", {
                "message": "Passwords must match."
            })

        
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "chat/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "chat/register.html")