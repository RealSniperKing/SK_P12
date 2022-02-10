from django.db import models
import uuid

from django.db.models import ForeignKey
from datetime import datetime


class Client(models.Model):
    # Client id
    client_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # client contact
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(unique=True, max_length=255, blank=False)
    phone = models.CharField(max_length=12, blank=True)
    mobile = models.CharField(max_length=12, blank=True)

    # client address
    company_name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, blank=True)
    address_complement = models.CharField(max_length=200, blank=True)
    postal_code = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)

    # Keep track
    author = ForeignKey('accounts.User', related_name='author_user_id', on_delete=models.SET_NULL, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updating_time = models.DateTimeField(null=True)

    # Epic events, sales contact
    sales_contact = ForeignKey('accounts.User', related_name='_sales_user_id', on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        self.updating_time = datetime.now()
        super(Client, self).save(*args, **kwargs)
