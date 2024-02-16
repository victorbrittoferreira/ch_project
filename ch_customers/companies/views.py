from rest_framework.generics import ListCreateAPIView, UpdateAPIView

from .permissions import IsCreator
from .models import Company
from .serializers import CompanySerializer, CompanyMemberSerializer
from rest_framework.permissions import IsAuthenticated

class CompanyListCreateAPIView(ListCreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Company.objects.filter(creator=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(
            creator=user,
            members=[user]
        )


class CompanyMemberUpdateAPIView(UpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyMemberSerializer
    permission_classes = [IsAuthenticated, IsCreator]
    http_method_names = ['put']

