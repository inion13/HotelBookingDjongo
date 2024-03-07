from django.db import models
from django.contrib.auth.models import User


class Hotel(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=256)
    address = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.title


class Room(models.Model):
    HOTEL_ROOM_TYPES = [
        ('standard', 'Standard'),
        ('superior', 'Superior'),
        ('luxury', 'Luxury'),
        ('family', 'Family')
    ]

    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    description = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    room_type = models.CharField(max_length=20, choices=HOTEL_ROOM_TYPES)

    class Meta:
        unique_together = ['hotel', 'room_number']

    def __str__(self):
        return f'{self.room_number}'


class Reservation(models.Model):
    user = models.ForeignKey(User, related_name='reservations', on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, related_name='hotel_reservations', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='reservations', on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.PositiveIntegerField()

    def __str__(self):
        return f'Бронь в отеле "{self.hotel.title}", комната {self.room.room_number}'
    