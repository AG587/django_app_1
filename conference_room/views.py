from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
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
