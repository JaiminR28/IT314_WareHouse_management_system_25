from django.shortcuts import render
from django.http import JsonResponse
import random
import time
from agora_token_builder import RtcTokenBuilder
from .models import RoomMember
import json
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

def lobby(request):
    return render(request, 'base/lobby.html')

def room(request):
    return render(request, 'base/room.html')


def getToken(request):
    # print("I am here to get Token")
    appId = "afb3eccd1d124950896b0a61c1496fdc"
    appCertificate = "f20ba26dac26467cae3a001a6c73bf24"
    channelName = request.GET.get('channel')
    uid = random.randint(1, 500)
    expirationTimeInSeconds = 3600
    currentTimeStamp = int(time.time())
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1

    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)

    return JsonResponse({'token': token, 'uid': uid}, safe=False)


@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    print("********************************************************")
    print(data)
    member, created = RoomMember.objects.get_or_create(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )

    return JsonResponse({'name':data['name']}, safe=False)


def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')
    # name = request.GET.get('name')
    member = RoomMember.objects.get(
        uid=uid,
        room_name=room_name,
        # name=name,
    )
    print("#######################################")
    print(member.name)
    return JsonResponse({'name':member.name}, safe=False)

@csrf_exempt
def deleteMember(request):
    data = json.loads(request.body)
    member = RoomMember.objects.get(
        # name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
    )
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print(member.name)
    member.delete()
    return JsonResponse('Member deleted', safe=False)