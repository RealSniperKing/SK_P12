from django.db import models
import uuid

from django.db.models import ForeignKey
from datetime import datetime


class Customer(models.Model):
    # Client id
    client_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Manager id
    client_manager = ForeignKey('accounts.User', related_name='manager_client_id', on_delete=models.SET_NULL, null=True, blank=True)

    # client contact
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(unique=True, max_length=255, blank=False)
    phone = models.CharField(max_length=12, blank=True)
    mobile = models.CharField(max_length=12, blank=True)

    # client address
    company_name = models.CharField(max_length=200, unique=True)
    address = models.CharField(max_length=200, blank=True)
    address_complement = models.CharField(max_length=200, blank=True)
    postal_code = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)

    # Keep track
    author = ForeignKey('accounts.User', related_name='author_user_id', on_delete=models.SET_NULL, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updating_time = models.DateTimeField(null=True)

    # Epic events, sales contact
    sales_contact = ForeignKey('accounts.User', related_name='_sales_user_id', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.updating_time = datetime.now()
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.company_name


class Contract(models.Model):
    # Contract id
    contract_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Client id
    client = ForeignKey('crm.Customer', related_name='customer_client_id', on_delete=models.SET_NULL, null=True, blank=True)

    # Manager id
    contract_manager = ForeignKey('accounts.User', related_name='manager_contract_id', on_delete=models.SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=200, blank=False)

    # Optional fields
    class Status(models.TextChoices):
        ACHEMINEMENT = '0', 'Acheminement'
        NEGOCIATION = '1', 'Négociation'
        SIGNE = '2', 'Signé'
        TERMINE = '3', 'Terminé'

    status = models.CharField(max_length=64, choices=Status.choices, default=Status.ACHEMINEMENT)

    amount = models.FloatField(null=True, blank=True)
    payment_due = models.DateTimeField(null=True, blank=True)

    created_time = models.DateTimeField(auto_now_add=True)
    updating_time = models.DateTimeField(null=True)

    def save(self, *args, **kwargs):
        self.updating_time = datetime.now()
        super(Contract, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Event(models.Model):
    event_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    contract = ForeignKey('crm.Contract', related_name='event_contract_id', on_delete=models.SET_NULL, null=True, blank=True)

    event_manager = ForeignKey('accounts.User', related_name='event_manager_id', on_delete=models.SET_NULL, null=True, blank=True)

    name = models.CharField(max_length=200, blank=False)

    attendees = models.IntegerField(null=True, blank=True)

    date_event_start = models.DateTimeField(null=True, blank=True)
    date_event_end = models.DateTimeField(null=True, blank=True)
    notes = models.CharField(max_length=1024, null=True, blank=True)

    created_time = models.DateTimeField(auto_now_add=True)
    updating_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


