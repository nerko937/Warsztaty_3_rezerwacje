from django.db import models


class Room(models.Model):
	name = models.CharField(
		verbose_name='nazwa',
		max_length=64
	)
	capacity = models.PositiveSmallIntegerField(
		verbose_name='pojemność'
	)
	projector = models.BooleanField(
		verbose_name='projektor',
		default=False
	)

	class Meta:
		verbose_name = 'Sala'
		verbose_name_plural = 'Sale'

	def __str__(self):
		return self.name


class Reservation(models.Model):
	date = models.DateField(
		verbose_name='data'
	)
	room = models.ForeignKey(
		Room,
		on_delete=models.SET_NULL,
		null=True,
		verbose_name='Sala'
	)
	comment = models.TextField(
		verbose_name='komentarz',
		null=True,
		blank=True
	)

	class Meta:
		verbose_name = 'Rezerwacja'
		verbose_name_plural = 'Rezerwacje'

	def __str__(self):
		return f'{self.room.name} {self.date}'
