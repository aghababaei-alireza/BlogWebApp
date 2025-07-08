from celery import shared_task
from django.db.models import Q
from datetime import datetime
from .models import Token


@shared_task
def remove_inactive_tokens():
    """
    This task will be scheduled to run every day to remove inactive tokens.
    """
    Token.objects.filter(Q(_is_active=False) | Q(expired_at__lt=datetime.now())).delete()
    print("InActive tokens removed.")
