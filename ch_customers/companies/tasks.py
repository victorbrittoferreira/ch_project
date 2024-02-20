from celery import shared_task
from django.core.exceptions import ValidationError
from requests.exceptions import RequestException
from django.utils import timezone
from .serializers import CompanyDataSerializer
from .models import Company
import requests
from django.utils import timezone

RATE_LIMIT = '3/m'
RATE_LIMIT_BACKOFF = 20  
MAX_RETRIES = 3

import logging

logger = logging.getLogger(__name__)

@shared_task
def queue_company_updates():
    today = timezone.now().date()
    
    companies_to_update = Company.objects.filter(
        next_update_rf__date__lte=today
    ).exclude(status="INVALID_TAX_NUMBER")
    
    logger.debug(f"COMPANIES {companies_to_update}")

    queue = [update_company_info.delay(company.id, today) for company in companies_to_update]
    logger.debug(f"QUEUE {queue} LEN {len(queue)}")

    if not queue:
        logger.info("There is no company to be update.")

@shared_task(bind=True, rate_limit=RATE_LIMIT, max_retries=MAX_RETRIES)
def update_company_info(self, company_id: int, today: timezone.datetime):
    try:
        logger.debug(f"START - ID {company_id}")

        base_path = 'https://receitaws.com.br/v1/cnpj/'

        company = Company.objects.get(pk=company_id)
        complete_path = base_path + str(company.tax_number)

        response = requests.get(complete_path, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            message = data.get('message')

            if message == "ERROR" or message == "CNPJ inválido":
                logger.debug("INVALID TAX NUMBER")
                company.status = "INVALID_TAX_NUMBER"
                company.save()
                return 
            
            data = response.json()
            serializer = CompanyDataSerializer(data=data)
            if serializer.is_valid():

                logger.debug("VALIDATED DATA")
                validated_data = serializer.validated_data
                logger.debug(validated_data)
                for field in validated_data:
                    setattr(company, field, validated_data[field])
                company.last_update_rf = today
                company.next_update_rf = today + timezone.timedelta(days=30)

                company.save()
                logger.debug(f"END - ID {company.id}")

            
        elif response.status_code in [429, 504]:
            logger.debug(f"STATUS {response.status_code}")
            logger.debug(self.request.id)
            self.retry(countdown=RATE_LIMIT_BACKOFF)


    except RequestException as e:
        logger.debug(f"RequestException: {e}")
    except ValidationError as e:
        logger.debug(F"ValidationError: {e}")
    