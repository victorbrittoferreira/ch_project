from django.urls import path
from .views import CompanyListCreateAPIView

companies_prefix = 'api/v1/companies/'

urlpatterns = [
    path(companies_prefix, CompanyListCreateAPIView.as_view(), name='company-list-create'),
]
