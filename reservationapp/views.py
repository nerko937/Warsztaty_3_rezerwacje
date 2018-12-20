from django.shortcuts import render, redirect
from django.views import View
from .forms import RoomForm, ReservationForm, SearchForm
from .models import Room, Reservation
import datetime


TODAY = datetime.date.today()


class NewRoom(View):
	def get(self, request):
		form = RoomForm()
		return render(request, 'new_room.html', {'form': form})

	def post(self, request):
		form = RoomForm(request.POST)
		if form.is_valid():
			is_projector = True if request.POST.get('projector') else False
			Room.objects.create(
				name=request.POST.get('name'),
				capacity=request.POST.get('capacity'),
				projector=is_projector
			)
		return redirect('adres')


class ModifyRoom(View):
	def get(self, request, room_id):
		room = Room.objects.get(id=room_id)
		form = RoomForm(initial={
			'name': room.name,
			'capacity': room.capacity,
			'projector': room.projector
		})
		return render(request, 'new_room.html', {'form': form})

	def post(self, request, room_id):
		form = RoomForm(request.POST)
		if form.is_valid():
			is_projector = True if request.POST.get('projector') else False
			room = Room.objects.get(id=room_id)
			room.name = request.POST.get('name')
			room.capacity = request.POST.get('capacity')
			room.projector = is_projector
			room.save()
			return redirect('adres')


class SearchRoom(View):
	def get(self, request):
		form = SearchForm()
		return render(request, 'search_room.html', {'form': form})

	def post(self, request):
		rooms = Room.objects.all()
		reservations = Reservation.objects.all()

		room_name = request.POST.get('name')
		capacity = request.POST.get('capacity')
		projector = request.POST.get('projector')
		date = request.POST.get('date')

		if room_name:
			rooms = rooms.filter(name__contains=room_name)

		if capacity:
			rooms = rooms.filter(capacity__gte=capacity)

		if projector:
			rooms = rooms.filter(projector=True)

		if date:
			date = datetime.datetime.strptime(date, '%Y-%m-%d')
			# busy in specified date
			reservations = reservations.filter(date=date)
			# room id's that are busy
			reservations = [reservation.room.id for reservation in reservations]
			rooms = rooms.exclude(id__in=reservations)

		if rooms.exists() is False:
			msg = 'Brak wolnych sal dla podanych kryteriów wyszukiwania. Następuje przekierowanie...'
			return render(request, 'alert.html', {'msg': msg})

		return render(request, 'show_rooms.html', {'rooms': rooms})


def delete_room(request, room_id):
	Room.objects.get(id=room_id).delete()
	return redirect('adres')


def show_rooms(request):
	rooms = Room.objects.all()
	today_busy = Reservation.objects.filter(date=TODAY)
	today_busy = [b.room.id for b in today_busy]
	return render(request, 'show_rooms.html', {
		'rooms': rooms,
		'today_busy': today_busy
	})


def room(request, room_id):
	room = Room.objects.get(id=room_id)
	form = ReservationForm()
	busy_dates = Reservation.objects.all()
	busy_dates = busy_dates.filter(room__id=room_id)
	busy_dates = busy_dates.filter(date__gte=TODAY)
	busy_dates = ['{:%Y-%m-%d}'.format(d.date) for d in busy_dates]
	return render(request, 'room.html', {
		'room': room,
		'form': form,
		'busy_dates': busy_dates
	})


def reservate(request, room_id):
	busy_dates = Reservation.objects.filter(room__id=room_id)
	busy_dates = ['{:%Y-%m-%d}'.format(d.date) for d in busy_dates]

	reservation_date = request.POST.get('date')

	if reservation_date:
		r_datetime = datetime.datetime.strptime(reservation_date, "%Y-%m-%d").date()
		if reservation_date not in busy_dates and r_datetime >= TODAY:
			Reservation.objects.create(
				date=reservation_date,
				room=Room.objects.get(id=room_id),
				comment=request.POST.get('comment')
			)
			return redirect('adres')
		else:
			msg = '''Podałeś niewłaściwe dane.
					Data powinna być teraźniejsza i nie nakładać się z obecnymi rezerwacjami.
					Następuje przekierowanie...'''
			return render(request, 'alert.html', {
				'msg': msg,
				'room_id': room_id
			})
	else:
		msg = 'Pole "data" jest puste. Następuje przekierowanie...'
		return render(request, 'alert.html', {
			'msg': msg,
			'room_id': room_id
		})
