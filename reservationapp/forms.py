from django import forms


from .models import Room, Reservation

class RoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ('name', 'capacity', 'projector')


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ('date', 'room', 'comment')


class SearchForm(forms.Form):
    name = forms.CharField(
        required=False,
        label='Nazwa',
        max_length=64,
    )
    capacity = forms.IntegerField(
        required=False,
        label='Minimalna pojemność',
    )
    projector = forms.BooleanField(
        required=False,
        label='Projektor',
    )