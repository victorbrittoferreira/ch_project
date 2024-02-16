from rest_framework.generics import ListCreateAPIView
from .models import Company
from .serializers import CompanySerializer
from rest_framework.permissions import IsAuthenticated

class CompanyListCreateAPIView(ListCreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Company.objects.filter(creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
