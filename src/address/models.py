import uuid

from django.db import models


class Address(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    country = models.CharField(max_length=128, blank=False)
    state = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=128, blank=False)
    zip_code = models.CharField(max_length=32, blank=False)
    address_one = models.CharField(max_length=1024, blank=False)
    address_two = models.CharField(max_length=1024, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
