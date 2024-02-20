from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from .permissions import IsCreator
from .models import Company
from .serializers import CompanySerializer, CompanyMemberSerializer, MembersSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
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


class CompanyMemberListView(ListAPIView):
    serializer_class = MembersSerializer
    permission_classes = [IsAuthenticated, IsCreator]

    def get_queryset(self):
        company_id = self.kwargs['pk']
        company = Company.objects.get(pk=company_id)
        print(self.request.user)
        self.check_object_permissions(self.request, company)
        return company.members.all()