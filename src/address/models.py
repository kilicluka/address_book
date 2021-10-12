import uuid

from django.contrib.auth import get_user_model
from django.db import models


class Address(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    country = models.CharField(max_length=128, blank=False)
    state = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=False)
    zip_code = models.CharField(max_length=32, blank=False)
    address_one = models.CharField(max_length=1024, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(get_user_model(), through='UserAddress')

    class Meta:
        verbose_name = 'address'
        verbose_name_plural = 'addresses'
        db_table = 'addresses'
        get_latest_by = 'created_at'
        ordering = ('created_at',)
        unique_together = ('zip_code', 'address_one',)

        indexes = [
            models.Index(fields=('uuid',))
        ]

    def __str__(self):
        return f'{self.city}, {self.country} - {self.address_one}'


class UserAddress(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    additional_address_data = models.CharField(max_length=1024, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'user address'
        verbose_name_plural = 'user addresses'
        db_table = 'user_addresses'
        get_latest_by = 'created_at'
        ordering = ('created_at',)
        unique_together = ('user', 'address',)
