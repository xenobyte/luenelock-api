from rest_framework import generics, permissions
from .models import Lock
from .serializers import LockSerializer


class LockList(generics.ListCreateAPIView):
    queryset = Lock.objects.all()
    serializer_class = LockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Lock.objects.filter(user=user)


class LockDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'uuid'
    serializer_class = LockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        lock = Lock.objects.get(uuid=self.kwargs['uuid'])
        return Lock.objects.filter(user=user, uuid=lock.uuid)
