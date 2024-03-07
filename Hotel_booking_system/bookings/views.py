from rest_framework import viewsets, status, generics, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Hotel, Room, Reservation
from .serializers import HotelSerializer, RoomSerializer, ReservationSerializer, UserSerializer


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            serializer.save()
        else:
            return Response({"error": "Только суперпользователь может создавать отели."},
                            status=status.HTTP_403_FORBIDDEN)


class HotelRoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['room_type']
    ordering_fields = ['price', 'capacity']

    def get_queryset(self):
        queryset = super().get_queryset()
        date = self.request.query_params.get('date', None)
        capacity = self.request.query_params.get('capacity', None)
        room_type = self.request.query_params.get('room_type', None)
        if date:
            queryset = queryset.filter(available_dates=date)
        if capacity:
            queryset = queryset.filter(capacity=capacity)
        if room_type:
            queryset = queryset.filter(room_type=room_type)
        return queryset


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    def room_create(self, serializer):
        if self.request.user.is_superuser:
            serializer.save()
        else:
            return Response({"error": "Только суперпользователь может создавать комнаты."},
                            status=status.HTTP_403_FORBIDDEN)



class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        room = serializer.validated_data['room']
        check_in_date = serializer.validated_data['check_in_date']
        check_out_date = serializer.validated_data['check_out_date']
        if room.reservations.filter(check_in_date__lt=check_out_date, check_out_date__gt=check_in_date).exists():
            return Response({"error": "Room is already reserved for specified dates."},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4MzYwMTI3LCJpYXQiOjE3MDgzNTk4MjcsImp0aSI6Ijg3MjU4NzdiNTEyNzQwM2U4Y2Q0NzVjNDFkYjhhOTlmIiwidXNlcl9pZCI6M30.Ql6EJBYzGfHSKZfQK65gBDzeZ6KuhIxOo--HQBUJWqI