from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from conference_room.models import Room, Reservation


class NewRoom(View):

    def get(self, request):
        return render(request, "add_new_room_form.html")

    def post(self, request):
        new_room_name = request.POST.get("name")
        new_room_capacity = int(request.POST.get("capacity"))
        new_projector_availability = request.POST.get("projector")

        if not new_room_name:
            message = "Specify room name."
            return HttpResponse(message)

        try:
            Room.objects.get(room_name=new_room_name)
            message = "Room already exists in database."
            return HttpResponse(message)
        except Room.DoesNotExist:
            if new_room_capacity > 0:
                k = Room.objects.create(room_name=new_room_name, capacity=new_room_capacity,
                                        projector_availability=new_projector_availability)
                k.save()
                message = "Room successfully saved to database."
            else:
                message = "Room capacity must be a positive number."

        return HttpResponse(message)


class ShowRooms(View):

    def get(self, request):
        rooms = Room.objects.all()
        list_of_rooms = '<h1> Conference rooms list</h1>'
        for room in rooms:
            projector = "Projector available" if room.projector_availability else "No projector"
            list_of_rooms += f'''<p> <a href="/room/{room.id}/">{room.room_name}</a>, {room.capacity}, {projector} <p>
            <a href="/room/modify?id={room.id}"> Edit room </a>
            <a href="/room/delete?id={room.id}"> Delete room </a>
            <a href="/room/reserve?id={room.id}"> Book room </a>'''
        list_of_rooms += f'<p> Autor projektu: Anna Głowacka</p>'
        return HttpResponse(list_of_rooms)


def delete_room(request):
    room_id = request.GET.get("id")
    r = Room.objects.get(id=room_id)
    r.delete()
    return redirect('/room/')


class ModifyRoom(View):
    def get(self, request):
        room_id = request.GET.get("id")
        r = Room.objects.get(id=room_id)
        chosen_room = {
            "chosen_room": r.room_name,
        }
        return render(request, "modify_room_form.html", chosen_room)

    def post(self, request):
        old_room_name = request.POST.get("old_name")
        new_room_name = request.POST.get("new_name")
        new_room_capacity = int(request.POST.get("new_capacity"))
        new_projector_availability = request.POST.get("new_projector")

        if not new_room_name:
            message = "Specify new room name."
            return HttpResponse(message)

        try:
            Room.objects.get(room_name=new_room_name)
            message = "Room already exists in database."
            return HttpResponse(message)
        except Room.DoesNotExist:
            if new_room_capacity > 0:
                k = Room.objects.get(room_name=old_room_name)
                k.room_name = new_room_name
                k.capacity = new_room_capacity
                k.projector_availability = new_projector_availability
                k.save()
                return redirect('/room/')
