from django.urls import path
from .views import CompanyListCreateAPIView, CompanyMemberUpdateAPIView

companies_prefix = 'api/v1/companies/'
company_prefix = 'api/v1/company/'

urlpatterns = [
    path(company_prefix, CompanyListCreateAPIView.as_view(), name='company-list-create'),
    path(f'{company_prefix}<int:pk>/update_members/', CompanyMemberUpdateAPIView.as_view(), name='update_company_members'),
]
