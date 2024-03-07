from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Hotel, Room, Reservation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'title', 'description', 'address', 'rooms']

    rooms = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['id', 'hotel', 'room_number', 'description', 'price', 'capacity', 'room_type']


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ['id', 'user', 'hotel', 'room', 'check_in_date', 'check_out_date', 'guests']

    def get_fields(self):
        fields = super().get_fields()
        if 'hotel' in self.context['request'].data:
            hotel_id = int(self.context['request'].data['hotel'])
            fields['room'].queryset = Room.objects.filter(hotel_id=hotel_id)
        return fields
