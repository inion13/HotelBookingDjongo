import django_filters
from .models import Room


class RoomFilter(django_filters.FilterSet):
    class Meta:
        model = Room
        fields = {
            'room_type': ['exact'],
            'price': ['lt', 'gt'],
            'capacity': ['exact', 'lt', 'gt'],
        }