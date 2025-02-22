# views.py
from rest_framework import generics
from .models import Payouts
from .serializers import PayoutsSerializer
from rest_framework.permissions import AllowAny

class PayoutsCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = Payouts.objects.all()
    serializer_class = PayoutsSerializer

class PayoutsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    lookup_field = 'artisan__unique_id'
    queryset = Payouts.objects.all()
    serializer_class = PayoutsSerializer

    def get_object(self):
        unique_id = self.kwargs.get('artisan_unique_id')
        return generics.get_object_or_404(Payouts, artisan__unique_id=unique_id)